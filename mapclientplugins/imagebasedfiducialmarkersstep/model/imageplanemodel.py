from __future__ import division

import get_image_size

from opencmiss.utils.zinc import create_finite_element_field, create_square_2d_finite_element, \
    create_volume_image_field, create_material_using_image_field
from opencmiss.utils.maths.algorithms import calculate_line_plane_intersection


class ImagePlaneModel(object):

    def __init__(self, master_model):
        self._master_model = master_model
        self._region = None
        self._frame_count = -1
        self._scale_field = None
        self._duration_field = None
        self._image_based_material = None
        self._scaled_coordinate_field = None
        self._images_info = None
        self._image_dimensions = [-1, -1]

    def calculate_image_pixels_rectangle(self, top_left_mesh_location, bottom_right_mesh_location):
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

        return (int(top_left_values[0] + 0.5),
                self._image_dimensions[1] - int(top_left_values[1] + 0.5),
                int(bottom_right_values[0] - top_left_values[0] + 0.5),
                int(top_left_values[1] - bottom_right_values[1] + 0.5))

    @staticmethod
    def get_intersection_point(ray):
        return calculate_line_plane_intersection(ray[0], ray[1], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])

    def load_images(self, images_info):
        if images_info is not None:
            self._master_model.reset()
            self._images_info = images_info
            self._load_images(images_info.image_files())

    def _convert_point_coordinates(self, points):
        return [(point[0], self._image_dimensions[1] - point[1]) for point in points]

    def convert_to_model_coordinates(self, image_points):
        return self._convert_point_coordinates(image_points)

    def convert_to_image_coordinates(self, model_points):
        return self._convert_point_coordinates(model_points)

    def get_number_of_images(self):
        return len(self._images_info.image_files())

    def get_image_file_name_at(self, index):
        return self._images_info.image_files()[index]

    def get_image_width(self):
        return self._image_dimensions[0]

    def get_image_height(self):
        return self._image_dimensions[1]

    def _load_images(self, images):
        field_module = self._region.getFieldmodule()
        self._frame_count = len(images)
        if self._frame_count > 0:
            # Assume all images have the same dimensions.
            width, height = get_image_size.get_image_size(images[0])
            if width != -1 or height != -1:
                cache = field_module.createFieldcache()
                self._scale_field.assignReal(cache, [width, height, 1.0])
                frames_per_second = self._master_model.get_frames_per_second()
                duration = self._frame_count / frames_per_second
                self._duration_field.assignReal(cache, duration)
                self._image_dimensions = [width, height]
            image_field = create_volume_image_field(field_module, images)
            self._image_based_material = create_material_using_image_field(self._region, image_field)

    def get_frame_count(self):
        return self._frame_count

    def set_duration_value(self, frames_per_second):
        field_module = self._region.getFieldmodule()
        cache = field_module.createFieldcache()
        duration = self._frame_count / frames_per_second
        self._duration_field.assignReal(cache, duration)

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

    def get_duration_field(self):
        return self._duration_field

    def get_coordinate_field(self):
        return self._scaled_coordinate_field

    def get_region(self):
        return self._region

    def create_model(self):
        default_region = self._master_model.get_default_region()
        if self._region is not None:
            default_region.removeChild(self._region)

        self._region = default_region.createChild('images')
        coordinate_field = create_finite_element_field(self._region)
        field_module = self._region.getFieldmodule()
        self._scale_field = field_module.createFieldConstant([2, 3, 1])
        self._duration_field = field_module.createFieldConstant(1.0)
        offset_field = field_module.createFieldConstant([+0.5, +0.5, 0.0])
        scaled_coordinate_field = field_module.createFieldMultiply(self._scale_field, coordinate_field)
        self._scaled_coordinate_field = field_module.createFieldAdd(scaled_coordinate_field, offset_field)
        create_square_2d_finite_element(field_module, coordinate_field,
                                        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])
