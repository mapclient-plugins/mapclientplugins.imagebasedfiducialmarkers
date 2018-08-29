
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
        self._model.register_time_value_update_callback(self._update_time_value)
        self._model.register_frame_index_update_callback(self._update_frame_index)
        self._image_plane_model = model.get_image_plane_model()
        self._image_plane_scene = model.get_image_plane_scene()
        self._done_callback = None

        self._make_connections()

    def _make_connections(self):
        self._ui.sceneviewer_widget.graphicsInitialized.connect(self._graphics_initialized)
        self._ui.done_pushButton.clicked.connect(self._done_clicked)
        self._ui.timeValue_doubleSpinBox.valueChanged.connect(self._time_value_changed)
        self._ui.timePlayStop_pushButton.clicked.connect(self._time_play_stop_clicked)
        self._ui.frameIndex_spinBox.valueChanged.connect(self._frame_index_value_changed)
        self._ui.framesPerSecond_spinBox.valueChanged.connect(self._frames_per_second_value_changed)
        self._ui.timeLoop_checkBox.clicked.connect(self._time_loop_clicked)

    def _done_clicked(self):
        self._model.done()
        self._done_callback()

    def _graphics_initialized(self):
        """
        Callback for when SceneviewerWidget is initialised
        Set custom scene from model
        """
        scene_viewer = self._ui.sceneviewer_widget.getSceneviewer()
        if scene_viewer is not None:
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
        frame_count = self._image_plane_model.get_frame_count()
        self._ui.frameIndex_spinBox.setMaximum(frame_count + 1)
        value = self._model.get_frames_per_second()
        self._ui.timeValue_doubleSpinBox.setMaximum(frame_count / value)

    def _update_time_value(self, value):
        self._ui.timeValue_doubleSpinBox.blockSignals(True)
        frame_count = self._image_plane_model.get_frame_count()
        max_time_value = frame_count / self._ui.framesPerSecond_spinBox.value()

        if value > max_time_value:
            self._ui.timeValue_doubleSpinBox.setValue(max_time_value)
            self._time_play_stop_clicked()
        else:
            self._ui.timeValue_doubleSpinBox.setValue(value)
        self._ui.timeValue_doubleSpinBox.blockSignals(False)

    def _update_frame_index(self, value):
        self._ui.frameIndex_spinBox.blockSignals(True)
        self._ui.frameIndex_spinBox.setValue(value)
        self._ui.frameIndex_spinBox.blockSignals(False)

    def _time_value_changed(self, value):
        self._model.set_time_value(value)

    def _time_duration_changed(self, value):
        self._model.set_time_duration(value)

    def _time_play_stop_clicked(self):
        play_text = 'Play'
        stop_text = 'Stop'
        current_text = self._ui.timePlayStop_pushButton.text()
        if current_text == play_text:
            self._ui.timePlayStop_pushButton.setText(stop_text)
            self._model.play()
        else:
            self._ui.timePlayStop_pushButton.setText(play_text)
            self._model.stop()

    def _time_loop_clicked(self):
        self._model.set_time_loop(self._ui.timeLoop_checkBox.isChecked())

    def _frame_index_value_changed(self, value):
        self._model.set_frame_index(value)

    def _frames_per_second_value_changed(self, value):
        self._model.set_frames_per_second(value)
        self._ui.timeValue_doubleSpinBox.setMaximum(self._image_plane_model.get_frame_count() / value)
