from PySide import QtCore

from opencmiss.zinc.context import Context

from mapclientplugins.imagebasedfiducialmarkersstep.model.imageplanemodel import ImagePlaneModel
from mapclientplugins.imagebasedfiducialmarkersstep.scene.imageplanescene import ImagePlaneScene


class ImageBasedFiducialMarkersMasterModel(object):

    def __init__(self):
        self._settings = {
            'frames-per-second': 25,
            'time-loop': False
        }

        self._context = Context("ImageBasedFiducialMarkers")
        self._region_name = "image"
        self._default_region = self._context.getDefaultRegion()
        self._region = None

        timekeeper_module = self._context.getTimekeepermodule()
        self._timekeeper = timekeeper_module.getDefaultTimekeeper()
        self._timer = QtCore.QTimer()
        self._current_time = 0.0
        self._time_value_update = None
        self._frame_index_update = None

        self._image_plane_model = ImagePlaneModel(self)
        self._image_plane_scene = ImagePlaneScene(self)

        self._make_connections()

    def _make_connections(self):
        self._timer.timeout.connect(self._timeout)

    def _timeout(self):
        increment = 1000 / self._settings['frames-per-second'] / 1000
        duration = self._image_plane_model.get_frame_count() / self._settings['frames-per-second']
        if not self._settings['time-loop'] and (self._current_time + increment) > duration:
            self._current_time = duration + 1e-08
        else:
            self._current_time += increment
        if self._settings['time-loop'] and self._current_time > duration:
            self._current_time -= duration

        self._timekeeper.setTime(self._scale_current_time_to_timekeeper_time())
        self._time_value_update(self._current_time)
        frame_index = self._image_plane_model.get_frame_index_for_time(self._current_time,
                                                                       self._settings['frames-per-second']) + 1
        self._frame_index_update(frame_index)

    def _scale_current_time_to_timekeeper_time(self):
        scaled_time = 0.0
        duration = self._image_plane_model.get_frame_count() / self._settings['frames-per-second']
        if duration > 0:
            scaled_time = self._current_time / duration

        return scaled_time

    def register_frame_index_update_callback(self, frame_index_update_callback):
        self._frame_index_update = frame_index_update_callback

    def register_time_value_update_callback(self, time_value_update_callback):
        self._time_value_update = time_value_update_callback

    def set_frame_index(self, frame_index):
        frame_value = frame_index - 1
        self._current_time = self._image_plane_model.get_time_for_frame_index(frame_value, self._settings['frames-per-second'])
        self._timekeeper.setTime(self._scale_current_time_to_timekeeper_time())
        self._time_value_update(self._current_time)

    def set_time_value(self, time):
        self._current_time = time
        self._timekeeper.setTime(self._scale_current_time_to_timekeeper_time())
        frame_index = self._image_plane_model.get_frame_index_for_time(time, self._settings['frames-per-second']) + 1
        self._frame_index_update(frame_index)

    def set_frames_per_second(self, value):
        self._settings['frames-per-second'] = value

    def get_frames_per_second(self):
        return self._settings['frames-per-second']

    def set_time_loop(self, state):
        self._settings['time-loop'] = state

    def is_time_loop(self):
        return self._settings['time-loop']

    def play(self):
        self._timer.start(1000 / self._settings['frames-per-second'])

    def stop(self):
        self._timer.stop()

    def done(self):
        pass

    def get_context(self):
        return self._context

    def get_region(self):
        return self._region

    def get_scene(self):
        return self._region.getScene()

    def get_timekeeper(self):
        return self._timekeeper

    def set_time(self, value):
        pass

    def get_image_plane_model(self):
        return self._image_plane_model

    def get_image_plane_scene(self):
        return self._image_plane_scene

    def reset(self):
        if self._region:
            self._default_region.removeChild(self._region)
        self._region = self._default_region.createChild(self._region_name)
        self._image_plane_model.create_model()
        self._image_plane_scene.create_graphics()
