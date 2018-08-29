
from PySide import QtGui

from mapclientplugins.imagebasedfiducialmarkersstep.view.ui_imagebasedfiducialmarkerswidget\
    import Ui_ImageBasedFiducialMarkersWidget


class ImageBasedFiducialMarkersWidget(QtGui.QWidget):

    def __init__(self, model, parent=None):
        super(ImageBasedFiducialMarkersWidget, self).__init__(parent)
        self._ui = Ui_ImageBasedFiducialMarkersWidget()
        self._ui.setupUi(self)
        self._ui.sceneviewer_widget.setContext(model.get_context())

        self._model = model
        self._image_plane_model = model.get_image_plane_model()
        self._image_plane_scene = model.get_image_plane_scene()
        self._done_callback = None

        self._make_connections()

    def _make_connections(self):
        self._ui.sceneviewer_widget.graphicsInitialized.connect(self._graphics_initialized)
        self._ui.done_pushButton.clicked.connect(self._done_clicked)

    def _done_clicked(self):
        self._model.done()
        self._done_callback()

    def _graphics_initialized(self):
        """
        Callback for when SceneviewerWidget is initialised
        Set custom scene from model
        """
        sceneviewer = self._ui.sceneviewer_widget.getSceneviewer()
        if sceneviewer is not None:
            scene = self._model.get_scene()
            self._ui.sceneviewer_widget.setTumbleRate(0)
            self._ui.sceneviewer_widget.setScene(scene)
            self._view_all()

    def _view_all(self):
        if self._ui.sceneviewer_widget.getSceneviewer() is not None:
            self._ui.sceneviewer_widget.viewAll()

    def register_done_callback(self, done_callback):
        self._done_callback = done_callback

    def set_images_info(self, images_info):
        self._image_plane_model.load_images(images_info)
        self._image_plane_scene.set_image_material()
