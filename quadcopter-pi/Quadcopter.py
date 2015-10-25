import smbus
from MPU6050 import MPU6050
from PwmBoard import PwmBoard
from Motor import Motor
import time
__author__ = 'janco'


class Quadcopter():

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.pwm = PwmBoard(self.bus,0x40)
        motor1 = Motor(self.pwm,0)
        gyro = MPU6050(self.bus,0x68)
        gyro.start()
        time.sleep(1)
        while(True):
            x,y = gyro.getlastvalues()
            print(x,y)
            motor1.setPercentage(x)
            time.sleep(0.01)

if __name__ == "__main__":
    Quadcopter()