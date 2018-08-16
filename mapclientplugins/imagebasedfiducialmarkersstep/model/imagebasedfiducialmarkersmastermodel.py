from opencmiss.zinc.context import Context


class ImageBasedFiducialMarkersMasterModel(object):

    def __init__(self):
        self._context = Context("ImageBasedFiducialMarkers")
        self._region = self._context.createRegion()

    def done(self):
        pass

    def get_context(self):
        return self._context

    def get_scene(self):
        return self._region.getScene()
