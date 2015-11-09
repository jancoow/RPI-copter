import math
import threading
import time
__author__ = 'janco'


class UserInput(threading.Thread):


    def __init__(self, quadcopter):
        """Init class """
        self.running = True
        self.q = quadcopter
        threading.Thread.__init__(self)

    def run(self):
        while(self.running):
            try:
                input = raw_input('Input:')
                if(input == "exit"):
                    self.q.stop()
                else:
                    self.q.setWantedX(int(input))
            except ValueError:
                print "geen nummer"

    def stop(self):
        self.running = False