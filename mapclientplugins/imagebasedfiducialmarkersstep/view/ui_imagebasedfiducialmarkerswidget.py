# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapclientplugins\imagebasedfiducialmarkersstep\qt\imagebasedfiducialmarkerswidget.ui'
#
# Created: Thu Aug 16 15:17:49 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ImageBasedFiducialMarkersWidget(object):
    def setupUi(self, ImageBasedFiducialMarkersWidget):
        ImageBasedFiducialMarkersWidget.setObjectName("ImageBasedFiducialMarkersWidget")
        ImageBasedFiducialMarkersWidget.resize(870, 576)
        self.horizontalLayout = QtGui.QHBoxLayout(ImageBasedFiducialMarkersWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.controlPanel_groupBox = QtGui.QGroupBox(ImageBasedFiducialMarkersWidget)
        self.controlPanel_groupBox.setObjectName("controlPanel_groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.controlPanel_groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.done_pushButton = QtGui.QPushButton(self.controlPanel_groupBox)
        self.done_pushButton.setObjectName("done_pushButton")
        self.verticalLayout.addWidget(self.done_pushButton)
        self.horizontalLayout.addWidget(self.controlPanel_groupBox)
        self.sceneviewer_widget = SceneviewerWidget(ImageBasedFiducialMarkersWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sceneviewer_widget.sizePolicy().hasHeightForWidth())
        self.sceneviewer_widget.setSizePolicy(sizePolicy)
        self.sceneviewer_widget.setObjectName("sceneviewer_widget")
        self.horizontalLayout.addWidget(self.sceneviewer_widget)

        self.retranslateUi(ImageBasedFiducialMarkersWidget)
        QtCore.QMetaObject.connectSlotsByName(ImageBasedFiducialMarkersWidget)

    def retranslateUi(self, ImageBasedFiducialMarkersWidget):
        ImageBasedFiducialMarkersWidget.setWindowTitle(QtGui.QApplication.translate("ImageBasedFiducialMarkersWidget", "Image Based Fiducial Markers", None, QtGui.QApplication.UnicodeUTF8))
        self.controlPanel_groupBox.setTitle(QtGui.QApplication.translate("ImageBasedFiducialMarkersWidget", "Control Panel", None, QtGui.QApplication.UnicodeUTF8))
        self.done_pushButton.setText(QtGui.QApplication.translate("ImageBasedFiducialMarkersWidget", "Done", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget
