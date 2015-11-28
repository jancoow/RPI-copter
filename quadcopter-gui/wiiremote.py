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
        notconnected = True
        while(notconnected):
            try:
                wm = cwiid.Wiimote()
                notconnected = False
                wm.led = 1
                rpt_mode = cwiid.RPT_BTN
                rpt_mode ^=  cwiid.RPT_EXT
                wm.rpt_mode = rpt_mode

                print("CONNECTED")
            except RuntimeError:
                print("Nog niet connected")
        while(True):
            state = wm.state
            buttons = state['buttons']
            if(buttons & cwiid.BTN_UP):
                self.emit(QtCore.SIGNAL("throttle(int)"), (self.mainframe.getthrottle() + 5))
            if(buttons & cwiid.BTN_DOWN):
                self.emit(QtCore.SIGNAL("throttle(int)"), (self.mainframe.getthrottle() - 5))
            if(state['ext_type'] == cwiid.EXT_NUNCHUK):
                nunchuck = state['nunchuk']['stick']
                self.emit(QtCore.SIGNAL("pitch(int)"), (nunchuck[0]-125)/2)
                self.emit(QtCore.SIGNAL("roll(int)"), (nunchuck[1]-130)/2)
            time.sleep(0.1)

