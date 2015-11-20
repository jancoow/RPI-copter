import threading
from socket import *
import time
__author__ = 'janco'


class NetworkHandler:
    def __init__(self, quadcopter):
        self.networksend = NetworkSend(quadcopter)
        self.networksend.start()

        self.networkreceive = NetworkReceive(quadcopter)
        self.networkreceive.start()

    def stop(self):
        self.networkreceive.stop()
        self.networksend.stop()


class NetworkReceive(threading.Thread):
    def __init__(self, quadcopter):
        self.udpsocket = socket(AF_INET, SOCK_DGRAM)
        self.udpsocket.bind(('0.0.0.0', 2828))
        self.running = True
        self.quadcopter = quadcopter
        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            recv_data, addr = self.udpsocket.recvfrom(35)
            recv_data = recv_data.rstrip()
            data = recv_data.decode().split("|")
            n = int(data[0])
            try:
                if(n == 0):           #normal control
                    if(len(data) == 4):
                        self.quadcopter.setthrottle(int(data[1]))
                        self.quadcopter.setroll(int(data[2]))
                        self.quadcopter.setpitch(int(data[3]))
                if(n == 1):          #PID gain settings
                    if(len(data) == 4):
                        self.quadcopter.changepidgain(float(data[1]), float(data[2]), float(data[3]))
            except Exception:
                print "weird messages received, skip this one"


    def stop(self):
        self.udpsocket.close()
        self.running = False


class NetworkSend(threading.Thread):
    def __init__(self, quadcopter):
        self.running = True
        self.ip = "192.168.1.11"
        self.port = 2828
        self.udpsocket = socket(AF_INET, SOCK_DGRAM)
        self.quadcopter = quadcopter
        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            self.udpsocket.sendto('|'.join(map(str,self.quadcopter.getdata())), (self.ip, self.port))
            time.sleep(0.1)

    def stop(self):
        self.udpsocket.close()
        self.running = False
