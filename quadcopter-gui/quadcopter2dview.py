__author__ = 'janco'

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

class quadcopter2dview(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setGeometry(QtCore.QRect(240, 10, 441, 211))
        self.x_angle = 0
        self.y_angle = 0

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
        qp.end()

    def setCordinats(self,x,y):
        self.x_angle = x
        self.y_angle = y
        self.repaint()