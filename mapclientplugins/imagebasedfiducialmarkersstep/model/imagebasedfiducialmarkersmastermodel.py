from opencmiss.zinc.context import Context

from mapclientplugins.imagebasedfiducialmarkersstep.model.imageplanemodel import ImagePlaneModel
from mapclientplugins.imagebasedfiducialmarkersstep.scene.imageplanescene import ImagePlaneScene


class ImageBasedFiducialMarkersMasterModel(object):

    def __init__(self):
        self._context = Context("ImageBasedFiducialMarkers")
        self._region_name = "image"
        self._default_region = self._context.getDefaultRegion()
        self._region = None

        timekeeper_module = self._context.getTimekeepermodule()
        self._timekeeper = timekeeper_module.getDefaultTimekeeper()

        self._image_plane_model = ImagePlaneModel(self)
        self._image_plane_scene = ImagePlaneScene(self)

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
        self._scene = self._region.getScene()
        self._image_plane_model.create_model()
        self._image_plane_scene.create_graphics()
