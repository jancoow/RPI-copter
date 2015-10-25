from socket import *
from PyQt4 import QtGui, QtCore
__author__ = 'janco'

class udpsocket(QtCore.QThread):
    def __init__(self, Ui_Frame):
        address = ('192.168.1.11', 2828)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(address)
        self.frame = Ui_Frame
        print "server open op poort 2828"
        QtCore.QThread.__init__(self)

    def run(self):
        print "test"
        while(True):
            recv_data, addr = self.server_socket.recvfrom(23)
            recv_data = recv_data.rstrip()
            data = recv_data.split("|")
            print (data)
            if(len(data) == 6):
                self.lastdata = (int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]))
                self.emit(QtCore.SIGNAL("newdata(QString, QString, QString, QString, QString, QString)"), data[0],data[1],data[2],data[3],data[4],data[5])

    def getlastdata(self):
        return self.lastdata
