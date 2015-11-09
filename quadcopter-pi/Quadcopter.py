import smbus
from userinput import UserInput
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

        self.userinput = UserInput(self)
        self.userinput.start()

        self.running = True

        self.wantedx = 0.0
        time.sleep(1)

    def start(self):
        lasttime = time.time()

        yaw_pid = PID(3.0,  0.0,   0.8)
        throttle = 400
        while self.running:
            x,y = self.mpu6050.getlastvalues()
            delta_time =  time.time() - lasttime
            lasttime = time.time()

            yaw_pid_result = yaw_pid.Compute(x,self.wantedx,delta_time)
            self.motor1.update((throttle + yaw_pid_result))
            self.motor2.update((throttle + yaw_pid_result))
            self.motor3.update((throttle - yaw_pid_result))
            self.motor4.update((throttle - yaw_pid_result))

            #print("dt: " + str(delta_time) + "  1:" + str(self.motor1.getpwm()) + " 2:" + str(self.motor4.getpwm()) + "  x:" + str(x) + " y:" + str(y) + " yawpid:" + str(yaw_pid_result))

    def setWantedX(self, x):
        self.wantedx = x

    def stop(self):
        self.running = False
        self.userinput.stop()
        self.motor1.update(200)
        self.motor2.update(200)
        self.motor3.update(200)
        self.motor4.update(200)
        self.mpu6050.stop()

if __name__ == "__main__":
    q = Quadcopter()
    try:
        q.start()
    except KeyboardInterrupt:
        q.stop()
        sys.exit()
