__author__ = 'janco'

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

class quadcopter2dview(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(QtCore.QRect(240, 10, 441, 211))
        self.x_angle = 0
        self.y_angle = 0
        self.motor1 = self.motor2 = self.motor3 = self.motor4 = 0

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#FFA500')
        qp.setPen(color)
        qp.drawLine(130, 19, 300, 190)
        qp.drawLine(130, 190, 300, 23)
        qp.drawText(QtCore.QRect(0, 20, 80, 20), QtCore.Qt.AlignCenter, "X: "+str(self.x_angle))
        qp.drawText(QtCore.QRect(0, 40, 80, 20), QtCore.Qt.AlignCenter, "Y: "+str(self.y_angle))

        qp.drawText(QtCore.QRect(90, 0, 80, 20), QtCore.Qt.AlignCenter, "%: "+str(self.motor3))
        qp.drawText(QtCore.QRect(260, 0, 80, 20), QtCore.Qt.AlignCenter, "%: "+str(self.motor4))
        qp.drawText(QtCore.QRect(90, 150, 80, 20), QtCore.Qt.AlignCenter, "%: "+str(self.motor1))
        qp.drawText(QtCore.QRect(260, 150, 80, 20), QtCore.Qt.AlignCenter, "%: "+str(self.motor2))

        qp.end()

    def setCordinats(self,x,y, m1, m2, m3, m4):
        self.x_angle = x
        self.y_angle = y
        self.motor1 = m1
        self.motor2 = m2
        self.motor3 = m3
        self.motor4 = m4
        self.repaint()