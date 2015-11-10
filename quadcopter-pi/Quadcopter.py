import smbus
from userinput import UserInput
from networkhandler import NetworkHandler
import sys
from MPU6050 import MPU6050
from PwmBoard import PwmBoard
from Motor import Motor
from PID import PID
import time
__author__ = 'janco'


class Quadcopter():

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.pwm = PwmBoard(self.bus,0x40)
        self.motor1 = Motor(self.pwm,0)
        self.motor2 = Motor(self.pwm,1)
        self.motor3 = Motor(self.pwm,2)
        self.motor4 = Motor(self.pwm,3)

        self.mpu6050 = MPU6050(self.bus,0x68)
        self.mpu6050.start()

        #self.userinput = UserInput(self)
        #self.userinput.start()

        self.networkhandler = NetworkHandler(self)

        self.running = True

        self.pgain = 3.0
        self.igain = 0.0
        self.dgain = 0.9

        self.yaw_pid = PID(self.pgain,  self.igain,   self.dgain)


        self.wantedyaw = 0.0
        self.wantedpitch = 0.0
        self.throttle = 0.0;

        time.sleep(1)

    def start(self):
        lasttime = time.time()

        countertime = time.time()
        counter = 0
        while self.running:
            x, y = self.mpu6050.getlastvalues()
            delta_time = time.time() - lasttime
            lasttime = time.time()

            yaw_pid_result = self.yaw_pid.Compute(x, self.wantedyaw, delta_time)
            if self.throttle != 0:
                self.motor1.update((self.throttle + yaw_pid_result))
                self.motor2.update((self.throttle + yaw_pid_result))
                self.motor3.update((self.throttle - yaw_pid_result))
                self.motor4.update((self.throttle - yaw_pid_result))
            counter += 1
            if(time.time() - countertime > 1):
                print(counter)
                countertime = time.time()
                counter = 0

    def changepidgain(self, pgain, igain, dgain):
        self.yaw_pid.changegain(pgain, igain, dgain)

    def setyaw(self, yaw):
        if (yaw > -50) & (yaw < 50):
            self.wantedyaw = yaw

    def setpitch(self, pitch):
        if (pitch > -20) & (pitch < 20):
            self.wantedyaw = pitch

    def setthrottle(self, throttle):
        if throttle == 0:
            self.throttle = 0
            time.sleep(0.1)
            self.motor1.stop()
            self.motor2.stop()
            self.motor3.stop()
            self.motor4.stop()
        else:
            throttle = throttle * (((self.motor1.max - 180) - (self.motor1.min + 180)) / 100) + (self.motor1.min + 180)
            if (throttle > (self.motor1.min + 180)) & (throttle < (self.motor1.max - 180)):
                self.throttle = throttle

    def getdata(self):
        gx, gy, ax, ay, x, y = self.mpu6050.getextendedvalues()
        return gx, gy, ax, ay, x, y, self.motor1.getpercent(), self.motor2.getpercent(), self.motor3.getpercent(), self.motor4.getpercent()

    def stop(self):
        self.running = False
        self.userinput.stop()
        self.mpu6050.stop()
        time.sleep(1)
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()
        self.networkhandler.stop()

if __name__ == "__main__":
    q = Quadcopter()
    try:
        q.start()
    except KeyboardInterrupt:
        q.stop()
        sys.exit()
