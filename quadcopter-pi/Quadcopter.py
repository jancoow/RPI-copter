import smbus
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
        self.pwm = PwmBoard(self.bus, 0x40)
        self.motor1 = Motor(self.pwm, 0)
        self.motor2 = Motor(self.pwm, 1)
        self.motor3 = Motor(self.pwm, 2)
        self.motor4 = Motor(self.pwm, 3)

        self.mpu6050 = MPU6050(self.bus, 0x68)
        self.mpu6050.start()

        self.networkhandler = NetworkHandler(self)

        self.running = True

        self.pgain = 5.0
        self.igain = 0.01
        self.dgain = 1.5

        self.roll_pid = PID(self.pgain, self.igain, self.dgain)
        self.pitch_pid = PID(self.pgain, self.igain, self.dgain)
        self.yaw_pid = PID(self.pgain, self.igain, self.dgain)

        self.wantedroll = 0.0
        self.wantedpitch = 0.0
        self.throttle = 0.0

        time.sleep(1)

    def start(self):
        lasttime = time.time()
        time_diff = 0.01
        while self.running:
            self.mpu6050.read()
            time.sleep(time_diff - 0.005)
            x, y, z = self.mpu6050.getlastvalues()
            delta_time = time.time() - lasttime
            lasttime = time.time()

            roll_pid_result = self.roll_pid.Compute(x, self.wantedroll, delta_time)
            pitch_pid_result = self.pitch_pid.Compute(y, self.wantedpitch, delta_time)
            #yaw_pid_result = self.yaw_pid.Compute(z, 0, delta_time)
            yaw_pid_result = 0

            if self.throttle != 0:
                self.motor1.update((self.throttle + roll_pid_result + pitch_pid_result + yaw_pid_result))
                self.motor2.update((self.throttle + roll_pid_result - pitch_pid_result - yaw_pid_result))
                self.motor3.update((self.throttle - roll_pid_result - pitch_pid_result + yaw_pid_result))
                self.motor4.update((self.throttle - roll_pid_result + pitch_pid_result - yaw_pid_result))

    def changepidgain(self, pgain, igain, dgain):
        self.roll_pid.changegain(pgain, igain, dgain)
        self.pitch_pid.changegain(pgain, igain, dgain)

    def setroll(self, roll):
        if (roll > -50) & (roll < 50):
            self.wantedroll = roll

    def setpitch(self, pitch):
        if (pitch > -50) & (pitch < 50):
            self.wantedpitch = pitch

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
        gx, gy, ax, ay, x, y, z = self.mpu6050.getextendedvalues()
        return gx, gy, ax, ay, x, y, z, self.motor1.getpercent(), self.motor2.getpercent(), self.motor3.getpercent(), self.motor4.getpercent()

    def stop(self):
        self.running = False
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
