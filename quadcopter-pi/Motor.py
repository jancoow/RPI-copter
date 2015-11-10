__author__ = 'janco'

class Motor():
    #max = 1870
    max = 1200.0
    min = 220.0

    def __init__(self, pwmboard, pin):
        self.pwmboard = pwmboard
        self.pin = pin
        self.pwm = 200
        self.pwmboard.setPWM(self.pin,0,200)

    def update(self, pwm):
        if pwm > self.max:
            pwm = self.max
        elif pwm < self.min:
            pwm = self.min
        self.pwm = int(pwm)
        self.pwmboard.setPWM(self.pin, 0, self.pwm)

    def stop(self):
        self.pwmboard.setPWM(self.pin, 0, 200)
        self.pwm = 200

    def getpwm(self):
        return self.pwm

    def getpercent(self):
        return int(((self.pwm - self.min)/(self.max - self.min))*100.0)