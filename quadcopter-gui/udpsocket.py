from socket import *
from PyQt4 import QtGui, QtCore
__author__ = 'janco'

class udpsocket(QtCore.QThread):
    def __init__(self, Ui_Frame):
        address = ('192.168.1.21', 2828)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(address)
        self.frame = Ui_Frame
        print("server open op poort 2828")
        QtCore.QThread.__init__(self)

    def run(self):
        while(True):
            recv_data, addr = self.server_socket.recvfrom(35)
            recv_data = recv_data.rstrip()
            data = recv_data.decode().split("|")
            print (data)
            if(len(data) == 11):
                self.emit(QtCore.SIGNAL("newdata(QString, QString, QString, QString, QString, QString, QString, QString, QString, QString, QString)"), data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10])

    def sendcontrol(self, throttle, yaw, pitch):
        self.server_socket.sendto(("0|" + str(throttle) + "|" + str(yaw) + "|" + str(pitch)).encode(), ("192.168.1.59", 2828))

    def sendpid(self, pgain, igain, dgain):
        self.server_socket.sendto(("1|" + str(pgain) + "|" + str(igain) + "|" + str(dgain)).encode(), ("192.168.1.59", 2828))
