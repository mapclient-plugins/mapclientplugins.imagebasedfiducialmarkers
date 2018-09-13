import numpy as np

import get_image_size

from sparc.videotracking.processing import Processing

from opencmiss.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_LOCAL, \
    SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT
from opencmiss.zinc.field import FieldFindMeshLocation
from opencmiss.utils.zinc import createFiniteElementField, createSquare2DFiniteElement, createVolumeImageField, \
    createMaterialUsingImageField


class ImagePlaneModel(object):

    def __init__(self, master_model):
        self._master_model = master_model
        self._region = None
        self._frame_count = -1
        self._scale_field = None
        self._image_based_material = None
        self._scaled_coordinate_field = None
        self._images_info = None
        self._image_dimensions = [-1, -1]

    def _calculate_image_pixels_rectangle(self, top_left_mesh_location, bottom_right_mesh_location):
        """
        The origin for the rectangle in the image is the top left corner, the mesh locations are given from
        the bottom left corner.
        :param top_left_mesh_location:
        :param bottom_right_mesh_location:
        :return: Rectangle with origin at top left of image described by [x, y, width, height]
        """
        field_module = self._scaled_coordinate_field.getFieldmodule()
        field_module.beginChange()
        field_cache = field_module.createFieldcache()
        field_cache.setMeshLocation(top_left_mesh_location[0], top_left_mesh_location[1])
        _, top_left_values = self._scaled_coordinate_field.evaluateReal(field_cache, 3)
        field_cache.setMeshLocation(bottom_right_mesh_location[0], bottom_right_mesh_location[1])
        _, bottom_right_values = self._scaled_coordinate_field.evaluateReal(field_cache, 3)
        field_module.endChange()
        print(top_left_values, bottom_right_values)

        return (int(top_left_values[0] + 0.5),
                self._image_dimensions[1] - int(top_left_values[1] + 0.5),
                int(bottom_right_values[0] - top_left_values[0] + 0.5),
                int(top_left_values[1] - bottom_right_values[1] + 0.5))

    def convert_to_image_roi(self, scene_viewer, element, rectangle_description):
        """
        Return a description of the rectangle in image pixels.  The resulting description is [top left corner x and y,
        width, height].  E.g. (1, 0, 48, 140).

        :param scene_viewer:
        :param element:
        :param rectangle_description: top left and bottom right corners of the rectangle in NDC top left coordinates.
        :return: A tuple in image pixels (x, y, width, height) describing a rectangle.
        """
        x1 = rectangle_description[0]
        y1 = rectangle_description[1]
        x2 = rectangle_description[2]
        y2 = rectangle_description[3]
        top_left_mesh_location = _determine_the_mesh_location(
            scene_viewer, x1, y1, element, self._scaled_coordinate_field)
        bottom_right_mesh_location = _determine_the_mesh_location(
            scene_viewer, x2, y2, element, self._scaled_coordinate_field)

        return self._calculate_image_pixels_rectangle(top_left_mesh_location, bottom_right_mesh_location)

    def load_images(self, images_info):
        if images_info is not None:
            self._master_model.reset()
            self._images_info = images_info
            self._load_images(images_info.image_files())

    def analyse_roi(self, image_index, image_roi):
        p = Processing()
        p.read_image(self._images_info.image_files()[image_index])
        p.filter_and_threshold()
        p.mask_and_image(image_roi)
        key_points, dst = p.feature_detect()

        key_point_list = [[key_point.pt[0], self._image_dimensions[1] - key_point.pt[1]] for key_point in key_points]

        return key_point_list

    def _load_images(self, images):
        field_module = self._region.getFieldmodule()
        self._frame_count = len(images)
        if self._frame_count > 0:
            # Assume all images have the same dimensions.
            width, height = get_image_size.get_image_size(images[0])
            if width != -1 or height != -1:
                cache = field_module.createFieldcache()
                self._scale_field.assignReal(cache, [width + 1, height + 1, 1.0])
                self._image_dimensions = [width, height]
            image_field = createVolumeImageField(field_module, images)
            self._image_based_material = createMaterialUsingImageField(self._region, image_field)

    def get_frame_count(self):
        return self._frame_count

    def get_time_for_frame_index(self, index, frames_per_second):
        duration = self._frame_count / frames_per_second
        frame_separation = 1 / self._frame_count
        initial_offset = frame_separation / 2

        return (index * frame_separation + initial_offset) * duration

    def get_frame_index_for_time(self, time, frames_per_second):
        duration = self._frame_count / frames_per_second
        frame_separation = 1 / self._frame_count
        initial_offset = frame_separation / 2
        return int((time / duration - initial_offset) / frame_separation + 0.5)

    def get_material(self):
        return self._image_based_material

    def get_coordinate_field(self):
        return self._scaled_coordinate_field

    def get_region(self):
        return self._region

    def create_model(self):
        default_region = self._master_model.get_default_region()
        if self._region is not None:
            default_region.removeChild(self._region)

        self._region = default_region.createChild('images')
        coordinate_field = createFiniteElementField(self._region)
        field_module = self._region.getFieldmodule()
        self._scale_field = field_module.createFieldConstant([2, 3, 1])
        offset_field = field_module.createFieldConstant([-0.5, -0.5, 0.0])
        scaled_coordinate_field = field_module.createFieldMultiply(self._scale_field, coordinate_field)
        self._scaled_coordinate_field = field_module.createFieldAdd(scaled_coordinate_field, offset_field)
        # self._scaled_coordinate_field = field_module.createFieldMultiply(self._scale_field, coordinate_field)
        createSquare2DFiniteElement(field_module, coordinate_field,
                                    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])


def _determine_the_mesh_location(scene_viewer, x, y, element, coordinate_field):
    mesh = element.getMesh()
    field_module = mesh.getFieldmodule()
    field_module.beginChange()
    element_group = field_module.createFieldElementGroup(mesh)
    mesh_group = element_group.getMeshGroup()
    mesh_group.addElement(element)
    field_mouse_location = field_module.createFieldConstant([x, -y])

    field_scene_viewer_projection = field_module.createFieldSceneviewerProjection(
        scene_viewer, SCENECOORDINATESYSTEM_LOCAL, SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT)

    field_projection = field_module.createFieldProjection(coordinate_field, field_scene_viewer_projection)
    field_x_y_projection = field_module.createFieldComponent(field_projection, [1, 2])
    field_find_mesh_location = field_module.createFieldFindMeshLocation(field_mouse_location,
                                                                        field_x_y_projection, mesh_group)
    field_find_mesh_location.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_NEAREST)

    field_cache = field_module.createFieldcache()

    found_element, xi_location = field_find_mesh_location.evaluateMeshLocation(field_cache, 2)

    del field_cache
    del field_find_mesh_location
    del field_x_y_projection
    del field_projection
    del field_scene_viewer_projection
    del field_mouse_location
    del mesh_group
    del element_group
    del coordinate_field

    field_module.endChange()

    return found_element, xi_location
