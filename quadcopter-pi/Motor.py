__author__ = 'janco'

class Motor():
    #max = 1870
    max = 600
    min = 220
    def __init__(self, pwmboard, pin):
        self.pwmboard = pwmboard
        self.pin = pin
        self.pwm = 200
        self.pwmboard.setPWM(self.pin,0,200)

    def update(self, pwm):
        if(pwm > self.max):
            pwm = self.max
        elif(pwm < self.min):
            pwm = self.min
        self.pwm = int(pwm)
        self.pwmboard.setPWM(self.pin, 0, self.pwm)

    def getpwm(self):
        return self.pwm