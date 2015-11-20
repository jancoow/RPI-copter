from socket import *
from PyQt4 import QtGui, QtCore
import cwiid
import time
__author__ = 'janco'

class wiiremote(QtCore.QThread):
    def __init__(self, Ui_Frame):
        self.mainframe = Ui_Frame
        QtCore.QThread.__init__(self)

    def run(self):
        wm = cwiid.Wiimote()
        while(True):
            if (wm.state['buttons'] & cwiid.BTN_1):
                print ("button '1' pressed")
                time.sleep(0.01)

