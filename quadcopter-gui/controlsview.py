__author__ = 'janco'

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class controlsview(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(QtCore.QRect(700, 240, 441, 280))
        self.throttleSlider = QtGui.QSlider(self)
        self.throttleSlider.setGeometry(QtCore.QRect(20, 20, 21, 230))
        self.throttleSlider.setOrientation(QtCore.Qt.Vertical)
        self.throttleSlider.setInvertedAppearance(False)
        self.throttleSlider.setInvertedControls(False)

        self.rollSlider = QtGui.QSlider(self)
        self.rollSlider.setGeometry(QtCore.QRect(150, 20, 21, 230))
        self.rollSlider.setMinimum(-100)
        self.rollSlider.setMaximum(100)
        self.rollSlider.setOrientation(QtCore.Qt.Vertical)
        self.rollSlider.setInvertedAppearance(False)
        self.rollSlider.setInvertedControls(False)

        self.pitchSlider = QtGui.QSlider(self)
        self.pitchSlider.setGeometry(QtCore.QRect(280, 20, 21, 230))
        self.pitchSlider.setMinimum(-100)
        self.pitchSlider.setMaximum(100)
        self.pitchSlider.setOrientation(QtCore.Qt.Vertical)
        self.pitchSlider.setInvertedAppearance(False)
        self.pitchSlider.setInvertedControls(False)

        self.submitbutton = QPushButton(self)
        self.submitbutton.setEnabled(1)
        self.submitbutton.setGeometry(QRect(390,0,49,21))
        self.submitbutton.setText("Apply")

        self.pedit = QLineEdit(self)
        self.pedit.setGeometry(QRect(280,0, 30,21))
        self.pedit.setText("3.1")

        self.iedit = QLineEdit(self)
        self.iedit.setGeometry(QRect(315,0, 30,21))
        self.iedit.setText("0.0")

        self.dedit = QLineEdit(self)
        self.dedit.setGeometry(QRect(350,0, 30,21))
        self.dedit.setText("0.9")



    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#FFA500')
        qp.setPen(color)
        qp.drawText(QtCore.QRect(40, 120, 80, 20), QtCore.Qt.AlignCenter, "Throttle "+str(self.throttleSlider.value()) + "%")
        qp.drawText(QtCore.QRect(170, 120, 80, 20), QtCore.Qt.AlignCenter, "Roll " + str(self.rollSlider.value()) + "º")
        qp.drawText(QtCore.QRect(300, 120, 80, 20), QtCore.Qt.AlignCenter, "Pitch "+str(self.pitchSlider.value()) + "º")
        qp.end()