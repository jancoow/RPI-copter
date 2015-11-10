import threading
__author__ = 'janco'


class UserInput(threading.Thread):
    def __init__(self, quadcopter):
        self.running = True
        self.q = quadcopter
        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            try:
                uinput = raw_input('Input:')
                if uinput == "exit":
                    self.q.stop()
                else:
                    self.q.setyaw(int(uinput))
            except ValueError:
                print "geen nummer"

    def stop(self):
        self.running = False
