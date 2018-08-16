from opencmiss.zinc.context import Context

from mapclientplugins.imagebasedfiducialmarkersstep.model.imageplanemodel import ImagePlaneModel


class ImageBasedFiducialMarkersMasterModel(object):

    def __init__(self):
        self._context = Context("ImageBasedFiducialMarkers")
        self._region = self._context.createRegion()

        self._image_plane_model = ImagePlaneModel()

    def done(self):
        pass

    def get_context(self):
        return self._context

    def get_scene(self):
        return self._region.getScene()

    def get_image_plane_model(self):
        return self._image_plane_model
