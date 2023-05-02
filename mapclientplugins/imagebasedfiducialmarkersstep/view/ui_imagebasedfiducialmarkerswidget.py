# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imagebasedfiducialmarkerswidget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from cmlibs.widgets.basesceneviewerwidget import BaseSceneviewerWidget

class Ui_ImageBasedFiducialMarkersWidget(object):
    def setupUi(self, ImageBasedFiducialMarkersWidget):
        if not ImageBasedFiducialMarkersWidget.objectName():
            ImageBasedFiducialMarkersWidget.setObjectName(u"ImageBasedFiducialMarkersWidget")
        ImageBasedFiducialMarkersWidget.resize(870, 576)
        self.horizontalLayout = QHBoxLayout(ImageBasedFiducialMarkersWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.controlPanel_groupBox = QGroupBox(ImageBasedFiducialMarkersWidget)
        self.controlPanel_groupBox.setObjectName(u"controlPanel_groupBox")
        self.verticalLayout = QVBoxLayout(self.controlPanel_groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.time_groupBox = QGroupBox(self.controlPanel_groupBox)
        self.time_groupBox.setObjectName(u"time_groupBox")
        self.gridLayout_4 = QGridLayout(self.time_groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.timePlayStop_pushButton = QPushButton(self.time_groupBox)
        self.timePlayStop_pushButton.setObjectName(u"timePlayStop_pushButton")

        self.gridLayout_4.addWidget(self.timePlayStop_pushButton, 1, 1, 1, 1)

        self.timeValue_label = QLabel(self.time_groupBox)
        self.timeValue_label.setObjectName(u"timeValue_label")

        self.gridLayout_4.addWidget(self.timeValue_label, 0, 0, 1, 1)

        self.timeValue_doubleSpinBox = QDoubleSpinBox(self.time_groupBox)
        self.timeValue_doubleSpinBox.setObjectName(u"timeValue_doubleSpinBox")
        self.timeValue_doubleSpinBox.setMaximum(12000.000000000000000)

        self.gridLayout_4.addWidget(self.timeValue_doubleSpinBox, 0, 1, 1, 1)

        self.timeLoop_checkBox = QCheckBox(self.time_groupBox)
        self.timeLoop_checkBox.setObjectName(u"timeLoop_checkBox")

        self.gridLayout_4.addWidget(self.timeLoop_checkBox, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.time_groupBox)

        self.video_groupBox = QGroupBox(self.controlPanel_groupBox)
        self.video_groupBox.setObjectName(u"video_groupBox")
        self.gridLayout_2 = QGridLayout(self.video_groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frameIndex_label = QLabel(self.video_groupBox)
        self.frameIndex_label.setObjectName(u"frameIndex_label")

        self.gridLayout_2.addWidget(self.frameIndex_label, 0, 0, 1, 1)

        self.framesPerSecond_spinBox = QSpinBox(self.video_groupBox)
        self.framesPerSecond_spinBox.setObjectName(u"framesPerSecond_spinBox")
        self.framesPerSecond_spinBox.setMinimum(1)
        self.framesPerSecond_spinBox.setValue(25)

        self.gridLayout_2.addWidget(self.framesPerSecond_spinBox, 1, 1, 1, 1)

        self.framesPerSecond_label = QLabel(self.video_groupBox)
        self.framesPerSecond_label.setObjectName(u"framesPerSecond_label")

        self.gridLayout_2.addWidget(self.framesPerSecond_label, 1, 0, 1, 1)

        self.frameIndex_spinBox = QSpinBox(self.video_groupBox)
        self.frameIndex_spinBox.setObjectName(u"frameIndex_spinBox")
        self.frameIndex_spinBox.setMinimum(1)
        self.frameIndex_spinBox.setMaximum(10000)

        self.gridLayout_2.addWidget(self.frameIndex_spinBox, 0, 1, 1, 1)

        self.numFrames_frame = QFrame(self.video_groupBox)
        self.numFrames_frame.setObjectName(u"numFrames_frame")
        self.numFrames_frame.setFrameShape(QFrame.StyledPanel)
        self.numFrames_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.numFrames_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.numFrames_label = QLabel(self.numFrames_frame)
        self.numFrames_label.setObjectName(u"numFrames_label")

        self.horizontalLayout_4.addWidget(self.numFrames_label)

        self.numFramesValue_label = QLabel(self.numFrames_frame)
        self.numFramesValue_label.setObjectName(u"numFramesValue_label")

        self.horizontalLayout_4.addWidget(self.numFramesValue_label)


        self.gridLayout_2.addWidget(self.numFrames_frame, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.video_groupBox)

        self.tracking_groupBox = QGroupBox(self.controlPanel_groupBox)
        self.tracking_groupBox.setObjectName(u"tracking_groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.tracking_groupBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.track_pushButton = QPushButton(self.tracking_groupBox)
        self.track_pushButton.setObjectName(u"track_pushButton")

        self.horizontalLayout_5.addWidget(self.track_pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.tracking_groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.groupBox = QGroupBox(self.controlPanel_groupBox)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.statusText_label = QLabel(self.groupBox)
        self.statusText_label.setObjectName(u"statusText_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusText_label.sizePolicy().hasHeightForWidth())
        self.statusText_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.statusText_label)


        self.verticalLayout.addWidget(self.groupBox)

        self.frame = QFrame(self.controlPanel_groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.done_pushButton = QPushButton(self.frame)
        self.done_pushButton.setObjectName(u"done_pushButton")

        self.horizontalLayout_2.addWidget(self.done_pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.frame)


        self.horizontalLayout.addWidget(self.controlPanel_groupBox)

        self.sceneviewer_widget = BaseSceneviewerWidget(ImageBasedFiducialMarkersWidget)
        self.sceneviewer_widget.setObjectName(u"sceneviewer_widget")
        sizePolicy.setHeightForWidth(self.sceneviewer_widget.sizePolicy().hasHeightForWidth())
        self.sceneviewer_widget.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.sceneviewer_widget)


        self.retranslateUi(ImageBasedFiducialMarkersWidget)

        QMetaObject.connectSlotsByName(ImageBasedFiducialMarkersWidget)
    # setupUi

    def retranslateUi(self, ImageBasedFiducialMarkersWidget):
        ImageBasedFiducialMarkersWidget.setWindowTitle(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Image Based Fiducial Markers", None))
        self.controlPanel_groupBox.setTitle(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Control Panel", None))
        self.time_groupBox.setTitle(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Time:", None))
        self.timePlayStop_pushButton.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Play", None))
        self.timeValue_label.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Time value:", None))
        self.timeLoop_checkBox.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Loop", None))
        self.video_groupBox.setTitle(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Video:", None))
        self.frameIndex_label.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Frame index:", None))
        self.framesPerSecond_label.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Frames per second:", None))
        self.numFrames_label.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"# frames:", None))
        self.numFramesValue_label.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"TextLabel", None))
        self.tracking_groupBox.setTitle(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Tracking:", None))
        self.track_pushButton.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Track", None))
        self.groupBox.setTitle("")
        self.statusText_label.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"TextLabel", None))
        self.done_pushButton.setText(QCoreApplication.translate("ImageBasedFiducialMarkersWidget", u"Done", None))
    # retranslateUi

