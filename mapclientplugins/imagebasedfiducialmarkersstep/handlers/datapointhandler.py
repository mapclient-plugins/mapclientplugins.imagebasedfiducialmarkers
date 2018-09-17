from opencmiss.zinc.sceneviewerinput import Sceneviewerinput
from opencmiss.zinchandlers.keyactivatedhandler import KeyActivatedHandler
from opencmiss.zinchandlers.abstracthandler import BUTTON_MAP


class DataPointHandler(KeyActivatedHandler):

    def __init__(self, key_code):
        super(DataPointHandler, self).__init__(key_code)
        self._model = None
        self._active_node = None

    def set_model(self, model):
        self._model = model

    def enter(self):
        pass

    def leave(self):
        pass

    def _get_ray(self, x, y):
        near_plane_point = self._scene_viewer.unproject(x, -y, 1.0)
        far_plane_point = self._scene_viewer.unproject(x, -y, -1.0)
        return [near_plane_point, far_plane_point]

    def mouse_press_event(self, event):
        super(DataPointHandler, self).mouse_press_event(event)
        if self._processing_mouse_events:
            x = event.x()
            y = event.y()
            node = self._scene_viewer.get_nearest_node(x, y)
            if node and node.isValid():
                self._model.select_node(node.getIdentifier())
            else:
                ray = self._get_ray(x, y)
                node = self._model.create_new_data_point(ray)

            self._active_node = node

    def mouse_move_event(self, event):
        super(DataPointHandler, self).mouse_move_event(event)
        if self._processing_mouse_events and self._active_node:
            x = event.x()
            y = event.y()
            ray = self._get_ray(x, y)
            self._model.set_node_location(self._active_node, ray)

    def mouse_release_event(self, event):
        super(DataPointHandler, self).mouse_release_event(event)
        if self._processing_mouse_events and self._active_node:
            if BUTTON_MAP[event.button()] == Sceneviewerinput.BUTTON_TYPE_RIGHT:
                self._model.remove_node(self._active_node.getIdentifier())
            else:
                self._model.deselect_node(self._active_node.getIdentifier())

            self._active_node = None

