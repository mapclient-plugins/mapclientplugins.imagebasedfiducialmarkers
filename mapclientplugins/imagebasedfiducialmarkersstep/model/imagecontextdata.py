

class ImageContextData(object):

    def __init__(self, context, frames_per_second, image_file_names):
        self._context = context
        self._frames_per_second = frames_per_second
        self._image_file_names = image_file_names

    def get_context(self):
        return self._context

    def get_frames_per_second(self):
        return self._frames_per_second

    def get_frame_count(self):
        return len(self._image_file_names)

    def get_image_file_names(self):
        return self._image_file_names
