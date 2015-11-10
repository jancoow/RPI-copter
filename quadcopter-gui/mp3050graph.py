__author__ = 'janco'

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
import pyqtgraph as pg
import math
import numpy as np

class mp3050graph(pg.PlotWidget):
    def __init__(self, parent = None):
        pg.PlotWidget.__init__(self, parent)
        self.data = [[],[],[],[],[],[]]
        self.setGeometry(QtCore.QRect(240, 240, 441, 281))
        self.curve1,self.curve2,self.curve3,self.curve4,self.curve5,self.curve6 = self.plot(), self.plot(),self.plot(),self.plot(),self.plot(),self.plot()


    def plotdata(self):
        for i in range(6):
            self.plot(range(0,len(self.data[0])), self.data[i], pen=(math.ceil(i/2),3), name='red plot')


    def adddata(self,gyrx,gyry,accx,accy,filterx,filtery):
        self.data[0].extend([float(gyrx)])
        self.data[1].extend([float(gyry)])
        self.data[2].extend([float(accx)])
        self.data[3].extend([float(accy)])
        self.data[4].extend([float(filterx)])
        self.data[5].extend([float(filtery)])
        self.curve1.setData(self.data[0], pen=(1,3))
        self.curve2.setData(self.data[1], pen=(1,3))
        self.curve3.setData(self.data[2], pen=(2,3))
        self.curve4.setData(self.data[3], pen=(2,3))
        self.curve5.setData(self.data[4], pen=(3,3))
        self.curve6.setData(self.data[5], pen=(3,3))
        if(len(self.data[0]) > 80):
             for i in range(6):
                self. data[i].pop(0)

