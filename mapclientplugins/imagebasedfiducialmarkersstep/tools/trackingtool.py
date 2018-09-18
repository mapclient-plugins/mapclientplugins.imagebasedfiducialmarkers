

class TrackingTool(object):

    def __init__(self, points_model, plane_model):
        self._points_model = points_model
        self._plane_model = plane_model

    def track_key_points(self):
        key_points = self._points_model.get_key_points()
        self._plane_model.track_key_points(key_points)

    def analyse_roi(self, image_index, zinc_sceneviewer, element, rectangle_description):
        image_roi = self._plane_model.convert_to_image_roi(zinc_sceneviewer, element, rectangle_description)
        key_points = self._plane_model.analyse_roi(image_index, image_roi)
        self._points_model.create_key_points(key_points)
