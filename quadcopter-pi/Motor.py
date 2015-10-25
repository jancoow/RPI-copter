__author__ = 'janco'

class Motor():
    max = 1700
    min = 1000
    def __init__(self, pwmboard, pin):
        self.pwmboard = pwmboard
        self.pin = pin
        self.pwmboard.setPWM(self.pin,0,200)

    def setPercentage(self, p):
        if(p<1):
            self.p = 1
        elif(p>100):
            self.p = 100
        else:
            self.p = p
        self.pwmboard.setPWM(self.pin,0,(int)(((self.p/100)*(self.max-self.min))+self.min))

    def getPercentage(self):
        return self.p
