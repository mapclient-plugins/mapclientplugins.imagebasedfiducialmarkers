
import get_image_size

from opencmiss.utils.zinc import createFiniteElementField, createSquare2DFiniteElement, createVolumeImageField, \
    createMaterialUsingImageField


class ImagePlaneModel(object):

    def __init__(self, master_model):
        self._master_model = master_model
        self._frame_count = -1
        self._scale_field = None
        self._image_based_material = None
        self._scaled_coordinate_field = None

    def load_images(self, images_info):
        if images_info is not None:
            self._master_model.reset()
            images = images_info.image_files()
            self._load_images(images)

    def _load_images(self, images):
        region = self._master_model.get_region()
        field_module = region.getFieldmodule()
        self._frame_count = len(images)
        if self._frame_count > 0:
            # Assume all images have the same dimensions.
            width, height = get_image_size.get_image_size(images[0])
            if width != -1 or height != -1:
                cache = field_module.createFieldcache()
                self._scale_field.assignReal(cache, [width, height, 1.0])
            image_field = createVolumeImageField(field_module, images)
            self._image_based_material = createMaterialUsingImageField(region, image_field)

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

    def create_model(self):
        region = self._master_model.get_region()
        coordinate_field = createFiniteElementField(region)
        field_module = region.getFieldmodule()
        self._scale_field = field_module.createFieldConstant([2, 3, 1])
        self._scaled_coordinate_field = field_module.createFieldMultiply(self._scale_field, coordinate_field)
        createSquare2DFiniteElement(field_module, coordinate_field,
                                    [[-0.5, -0.5, 0.0], [0.5, -0.5, 0.0], [-0.5, 0.5, 0.0], [0.5, 0.5, 0.0]])
