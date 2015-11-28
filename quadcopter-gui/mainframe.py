import sys
from PyQt4 import QtCore, QtGui, Qt
from quadcopter2dview import quadcopter2dview
from quadcopter3dview import quadcopter3dview
from mp3050graph import mp3050graph
from controlsview import controlsview
from udpsocket import udpsocket
from ps3controller import ps3controller

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Frame(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(32,32,32))
        self.setPalette(p)
        #self.wiiremote = wiiremote(self)
        #self.wiiremote.start()
        self.ps3controller = ps3controller(self)
        self.ps3controller.start()
        self.setupUi(self)
        self.networkhandler = udpsocket(self)
        self.networkhandler.start()
        self.connect(self.networkhandler, QtCore.SIGNAL("newdata(QString, QString, QString, QString, QString, QString, QString, QString, QString, QString, QString)"), self.newdata)
        self.throttle = self.pitch = self.roll = 0

    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.setWindowModality(QtCore.Qt.WindowModal)
        Frame.setFixedSize(1150, 528)
        self.widget = QtGui.QWidget(Frame)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1150, 531))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.line = QtGui.QFrame(self.widget)
        self.line.setGeometry(QtCore.QRect(220, 0, 20, 531))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        #statics table left upper
        self.Statics = QtGui.QTableWidget(self.widget)
        self.Statics.setGeometry(QtCore.QRect(10, 10, 211, 211))
        self.Statics.setObjectName(_fromUtf8("tableView"))
        self.Statics.setRowCount(6)
        self.Statics.setColumnCount(2)
        self.Statics.setItem(0, 0, QtGui.QTableWidgetItem("Connected:"))
        self.Statics.setItem(1, 0, QtGui.QTableWidgetItem("Signaal:"))
        self.Statics.setItem(2, 0, QtGui.QTableWidgetItem("Batterij:"))
        self.Statics.setItem(3, 0, QtGui.QTableWidgetItem("GPS lg,bg:"))
        self.Statics.setItem(4, 0, QtGui.QTableWidgetItem("GPS hoogte:"))
        self.Statics.setItem(5, 0, QtGui.QTableWidgetItem("GPS snelheid:"))
        self.Statics.verticalHeader().setVisible(False)
        self.Statics.horizontalHeader().setVisible(False)


        #log console links onderin
        self.scrollArea = QtGui.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 240, 211, 281))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 209, 270))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollAreaWidgetContents.setBackgroundRole(QtGui.QPalette.Dark)

        self.logConsole = QtGui.QTextBrowser(self.scrollAreaWidgetContents)
        self.logConsole.setGeometry(QtCore.QRect(-1, -1, 231, 291))
        self.logConsole.setObjectName(_fromUtf8("LogConsole"))
        self.logConsole.append("Starting motors...")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.line_2 = QtGui.QFrame(self.widget)
        self.line_2.setGeometry(QtCore.QRect(680, 0, 20, 531))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))

        self.line_3 = QtGui.QFrame(self.widget)
        self.line_3.setGeometry(QtCore.QRect(0, 215, 1150, 31))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))

        #control view
        self.controlsview = controlsview(self.widget)
        QtCore.QObject.connect(self.controlsview.throttleSlider, QtCore.SIGNAL('valueChanged(int)'), self.setthrottle)
        QtCore.QObject.connect(self.controlsview.rollSlider, QtCore.SIGNAL('valueChanged(int)'), self.setroll)
        QtCore.QObject.connect(self.controlsview.pitchSlider, QtCore.SIGNAL('valueChanged(int)'), self.setpitch)
        QtCore.QObject.connect(self.controlsview.submitbutton, QtCore.SIGNAL('clicked()'), self.sendpid)

        #wiiremote
        #QtCore.QObject.connect(self.wiiremote, QtCore.SIGNAL('throttle(int)'), self.setthrottle)
        #QtCore.QObject.connect(self.wiiremote, QtCore.SIGNAL('pitch(int)'), self.setpitch)
        #QtCore.QObject.connect(self.wiiremote, QtCore.SIGNAL('roll(int)'), self.setroll)

        #ps3controller
        QtCore.QObject.connect(self.ps3controller, QtCore.SIGNAL('throttle(int)'), self.setthrottle)
        QtCore.QObject.connect(self.ps3controller, QtCore.SIGNAL('pitch(int)'), self.setpitch)
        QtCore.QObject.connect(self.ps3controller, QtCore.SIGNAL('roll(int)'), self.setroll)

        #mp3050graph
        self.mp3050graph = mp3050graph(self.widget)

        #2d quadcopter view
        self.quadcopter2dview = quadcopter2dview(self.widget)

        #3d quadcopter view
        self.quadcopter3dview = quadcopter3dview(self.widget)

        QtCore.QMetaObject.connectSlotsByName(Frame)
        Frame.setWindowTitle(_translate("Frame", "Quadcopter GUI", None))

    def setroll(self,roll):
        self.roll = roll
        self.controlsview.rollSlider.setValue(roll)
        self.controlsview.repaint()
        self.sendcontrol()

    def setpitch(self, pitch):
        self.pitch = pitch
        self.controlsview.pitchSlider.setValue(pitch)
        self.controlsview.repaint()
        self.sendcontrol()

    def setthrottle(self, throttle):
        self.throttle = throttle
        self.controlsview.throttleSlider.setValue(throttle)
        self.controlsview.repaint()
        self.sendcontrol()

    def getthrottle(self):
        return int(self.controlsview.throttleSlider.value())

    def sendcontrol(self):
        self.networkhandler.sendcontrol(self.throttle, self.roll, self.pitch)

    def sendpid(self):
        self.networkhandler.sendpid(self.controlsview.pedit.text(), self.controlsview.iedit.text(), self.controlsview.dedit.text())

    def newdata(self, gyrx, gyry, accx, accy, filterx, filtery,z, m1, m2, m3, m4):
        self.quadcopter3dview.setCordinats(filterx,filtery)
        self.quadcopter2dview.setCordinats(filterx,filtery,z, m1, m2, m3, m4)
        self.mp3050graph.adddata(gyrx,gyry,accx,accy,filterx,filtery)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Frame()
    ex.show()
    sys.exit(app.exec_())
