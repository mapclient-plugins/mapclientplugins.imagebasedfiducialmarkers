
from PySide import QtGui, QtCore

from opencmiss.zinchandlers.scenemanipulation import SceneManipulation

from mapclientplugins.imagebasedfiducialmarkersstep.handlers.datapointadder import DataPointAdder
from mapclientplugins.imagebasedfiducialmarkersstep.handlers.datapointremover import DataPointRemover
from mapclientplugins.imagebasedfiducialmarkersstep.handlers.rectangletool import RectangleTool
from mapclientplugins.imagebasedfiducialmarkersstep.static.strings import DEFINE_ROI_STRING, \
    SET_INITIAL_TRACKING_POINTS_STRING, FINALISE_TRACKING_POINTS_STRING
from mapclientplugins.imagebasedfiducialmarkersstep.tools.datapointtool import DataPointTool
from mapclientplugins.imagebasedfiducialmarkersstep.tools.trackingtool import TrackingTool
from mapclientplugins.imagebasedfiducialmarkersstep.view.ui_imagebasedfiducialmarkerswidget\
    import Ui_ImageBasedFiducialMarkersWidget

PLAY_TEXT = 'Play'
STOP_TEXT = 'Stop'


class ImageBasedFiducialMarkersWidget(QtGui.QWidget):

    def __init__(self, model, parent=None):
        super(ImageBasedFiducialMarkersWidget, self).__init__(parent)
        self._ui = Ui_ImageBasedFiducialMarkersWidget()
        self._ui.setupUi(self)
        self._ui.sceneviewer_widget.set_context(model.get_context())

        self._settings = {'view-parameters': {}}

        self._model = model
        self._model.register_time_value_update_callback(self._update_time_value)
        self._model.register_frame_index_update_callback(self._update_frame_index)
        self._image_plane_scene = model.get_image_plane_scene()
        self._done_callback = None

        self._image_plane_model = model.get_image_plane_model()
        tracking_points_model = model.get_tracking_points_model()

        self._data_point_tool = DataPointTool(tracking_points_model, self._image_plane_model)
        self._tracking_tool = TrackingTool(tracking_points_model, self._image_plane_model)

        self._setup_handlers()
        self._set_initial_ui_state()
        self._update_ui_state()

        self._make_connections()

    def _make_connections(self):
        self._ui.sceneviewer_widget.graphics_initialized.connect(self._graphics_initialized)
        self._ui.done_pushButton.clicked.connect(self._done_clicked)
        self._ui.timeValue_doubleSpinBox.valueChanged.connect(self._time_value_changed)
        self._ui.timePlayStop_pushButton.clicked.connect(self._time_play_stop_clicked)
        self._ui.frameIndex_spinBox.valueChanged.connect(self._frame_index_value_changed)
        self._ui.framesPerSecond_spinBox.valueChanged.connect(self._frames_per_second_value_changed)
        self._ui.timeLoop_checkBox.clicked.connect(self._time_loop_clicked)
        self._ui.defineROI_pushButton.clicked.connect(self._define_roi_button_clicked)
        self._ui.setInitialTrackingPoints_pushButton.clicked.connect(self._set_initial_tracking_points_button_clicked)
        self._ui.finaliseTrackingPoints_radioButton.toggled.connect(self._radio_button_state_changed)
        self._ui.defineROI_radioButton.toggled.connect(self._radio_button_state_changed)
        self._ui.setInitialTrackingPoints_radioButton.toggled.connect(self._radio_button_state_changed)

    def _done_clicked(self):
        self._model.done()
        self._done_callback()

    def _graphics_initialized(self):
        """
        Callback for when SceneviewerWidget is initialised
        Set custom scene from model
        """
        scene_viewer = self._ui.sceneviewer_widget.get_zinc_sceneviewer()
        if scene_viewer is not None:
            scene = self._model.get_scene()
            self._ui.sceneviewer_widget.set_tumble_rate(0)
            self._ui.sceneviewer_widget.set_scene(scene)
            if len(self._settings['view-parameters']) == 0:
                self._view_all()
            else:
                eye = self._settings['view-parameters']['eye']
                look_at = self._settings['view-parameters']['look_at']
                up = self._settings['view-parameters']['up']
                angle = self._settings['view-parameters']['angle']
                self._ui.sceneviewer_widget.set_view_parameters(eye, look_at, up, angle)

    def _set_initial_ui_state(self):
        self._ui.framesPerSecond_spinBox.setValue(self._model.get_frames_per_second())
        self._ui.timeLoop_checkBox.setChecked(self._model.is_time_loop())
        self._ui.defineROI_radioButton.setChecked(True)
        self._enter_define_roi()
        minimum_label_width = self._calculate_minimum_label_width()
        self._ui.statusText_label.setMinimumWidth(minimum_label_width)

    def _calculate_minimum_label_width(self):
        label = self._ui.statusText_label
        label.setWordWrap(True)
        label.setText(DEFINE_ROI_STRING)
        maximum_width = 0
        width = label.fontMetrics().boundingRect(label.text()).width()
        maximum_width = max(maximum_width, width)
        label.setText(SET_INITIAL_TRACKING_POINTS_STRING)
        width = label.fontMetrics().boundingRect(label.text()).width()
        maximum_width = max(maximum_width, width)
        label.setText(FINALISE_TRACKING_POINTS_STRING)
        width = label.fontMetrics().boundingRect(label.text()).width()
        maximum_width = max(maximum_width, width)
        return maximum_width / 3.0

    def _update_ui_state(self):
        define_roi = self._ui.defineROI_radioButton.isChecked()
        self._ui.defineROI_pushButton.setEnabled(define_roi)
        set_initial_tracking_points = self._ui.setInitialTrackingPoints_radioButton.isChecked()
        self._ui.setInitialTrackingPoints_pushButton.setEnabled(set_initial_tracking_points)
        finalise_tracking_points = self._ui.finaliseTrackingPoints_radioButton.isChecked()
        if define_roi:
            self._ui.statusText_label.setText(DEFINE_ROI_STRING)
        elif set_initial_tracking_points:
            self._ui.statusText_label.setText(SET_INITIAL_TRACKING_POINTS_STRING)
        elif finalise_tracking_points:
            self._ui.statusText_label.setText(FINALISE_TRACKING_POINTS_STRING)

    def _radio_button_state_changed(self):
        sender = self.sender()
        object_name = sender.objectName()
        if sender.isChecked():
            self._update_ui_state()
            if 'defineROI' in object_name:
                self._enter_define_roi()
            elif 'setInitialTrackingPoints' in object_name:
                self._enter_set_initial_tracking_points()
            elif 'finaliseTrackingPoints' in object_name:
                self._enter_finalise_tracking_points()
        else:
            if 'defineROI' in object_name:
                self._leave_define_roi()
            elif 'setInitialTrackingPoints' in object_name:
                self._leave_set_initial_tracking_points()
            elif 'finaliseTrackingPoints' in object_name:
                self._leave_finalise_tracking_points()

    def _define_roi_button_clicked(self):
        self._ui.setInitialTrackingPoints_radioButton.setChecked(True)

    def _set_initial_tracking_points_button_clicked(self):
        self._ui.finaliseTrackingPoints_radioButton.setChecked(True)

    def _setup_handlers(self):
        basic_handler = SceneManipulation()
        self._ui.sceneviewer_widget.register_handler(basic_handler)
        self._rectangle_tool = RectangleTool(QtCore.Qt.Key_D)
        self._data_point_adder = DataPointAdder(QtCore.Qt.Key_A)
        self._data_point_adder.set_model(self._data_point_tool)
        self._data_point_remover = DataPointRemover(QtCore.Qt.Key_D)
        self._data_point_remover.set_model(self._data_point_tool)


    def _enter_define_roi(self):
        self._ui.sceneviewer_widget.register_handler(self._rectangle_tool)
        self._ui.sceneviewer_widget.register_key_listener(QtCore.Qt.Key_Return, self._define_roi_button_clicked)

    def _leave_define_roi(self):
        rectangle_description = self._rectangle_tool.get_rectangle_box_description()
        if sum(rectangle_description) < 0:
            QtGui.QMessageBox.warning(self, 'Invalid ROI', 'The region of interest is invalid and region'
                                      ' analysis will not be performed')
        else:
            self._rectangle_tool.remove_rectangle_box()
            self._ui.sceneviewer_widget.unregister_handler(self._rectangle_tool)
            self._ui.sceneviewer_widget.unregister_key_listener(QtCore.Qt.Key_Return)

            x = rectangle_description[0]
            y = rectangle_description[1]
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            element = self._ui.sceneviewer_widget.get_nearest_element(x, y)
            QtGui.QApplication.restoreOverrideCursor()
            if element.isValid():
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                image_index = self._ui.frameIndex_spinBox.value() - 1
                self._tracking_tool.analyse_roi(
                    image_index, self._ui.sceneviewer_widget.get_zinc_sceneviewer(), element, rectangle_description)
                QtGui.QApplication.restoreOverrideCursor()
            else:
                QtGui.QMessageBox.warning(self, 'Invalid ROI', 'The region of interest is invalid and region'
                                          ' analysis will not be performed')

    def _enter_set_initial_tracking_points(self):
        self._ui.sceneviewer_widget.register_handler(self._data_point_adder)
        self._ui.sceneviewer_widget.register_handler(self._data_point_remover)
        self._ui.sceneviewer_widget.register_key_listener(QtCore.Qt.Key_Return,
                                                          self._set_initial_tracking_points_button_clicked)

    def _leave_set_initial_tracking_points(self):
        self._ui.sceneviewer_widget.unregister_handler(self._data_point_adder)
        self._ui.sceneviewer_widget.unregister_handler(self._data_point_remover)
        self._ui.sceneviewer_widget.unregister_key_listener(QtCore.Qt.Key_Return)

        # Perform the tracking for all images.
        self._tracking_tool.track_key_points()

    def _enter_finalise_tracking_points(self):
        pass

    def _leave_finalise_tracking_points(self):
        pass

    def _view_all(self):
        if self._ui.sceneviewer_widget.get_zinc_sceneviewer() is not None:
            self._ui.sceneviewer_widget.view_all()

    def register_done_callback(self, done_callback):
        self._done_callback = done_callback

    def set_settings(self, settings):
        self._settings.update(settings)

    def get_settings(self):
        eye, look_at, up, angle = self._ui.sceneviewer_widget.get_view_parameters()
        self._settings['view-parameters'] = {'eye': eye, 'look_at': look_at, 'up': up, 'angle': angle}
        return self._settings

    def set_images_info(self, images_info):
        self._image_plane_model.load_images(images_info)
        self._image_plane_scene.set_image_material()
        frame_count = self._image_plane_model.get_frame_count()
        self._ui.frameIndex_spinBox.setMaximum(frame_count + 1)
        value = self._model.get_frames_per_second()
        self._ui.timeValue_doubleSpinBox.setMaximum(frame_count / value)
        self._ui.numFramesValue_label.setText("%d" % frame_count)
        self._model.set_frame_index(1)

    def _update_time_value(self, value):
        self._ui.timeValue_doubleSpinBox.blockSignals(True)
        frame_count = self._image_plane_model.get_frame_count()
        max_time_value = frame_count / self._ui.framesPerSecond_spinBox.value()

        if value > max_time_value:
            print(value, max_time_value)
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
        current_text = self._ui.timePlayStop_pushButton.text()
        if current_text == PLAY_TEXT:
            self._ui.timePlayStop_pushButton.setText(STOP_TEXT)
            self._model.play()
        else:
            self._ui.timePlayStop_pushButton.setText(PLAY_TEXT)
            self._model.stop()

    def _time_loop_clicked(self):
        self._model.set_time_loop(self._ui.timeLoop_checkBox.isChecked())

    def _frame_index_value_changed(self, value):
        self._model.set_frame_index(value)

    def _frames_per_second_value_changed(self, value):
        self._model.set_frames_per_second(value)
        self._ui.timeValue_doubleSpinBox.setMaximum(self._image_plane_model.get_frame_count() / value)
