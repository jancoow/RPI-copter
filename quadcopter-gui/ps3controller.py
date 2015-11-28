from socket import *
from PyQt4 import QtGui, QtCore
import pygame.joystick
import time

__author__ = 'janco'

class ps3controller(QtCore.QThread):
    def __init__(self, Ui_Frame):
        self.mainframe = Ui_Frame
        QtCore.QThread.__init__(self)
        self.setpoint = 100

    def run(self):
        pygame.init()
        pygame.joystick.init()
        print pygame.joystick.get_count()

        _joystick = pygame.joystick.Joystick(0)
        _joystick.init()
        print _joystick.get_init()
        print _joystick.get_id()
        print _joystick.get_name()
        print _joystick.get_numaxes()
        print _joystick.get_numballs()
        print _joystick.get_numbuttons()
        print _joystick.get_numhats()
        print _joystick.get_axis(0)

        axes = [ 0.0 ] * _joystick.get_numaxes()
        buttons = [ False ] * _joystick.get_numbuttons()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    e = event.dict
                    if(axes[e['axis']] != e['value']):
                        axes[e['axis']] = e['value']
                        self.emit(QtCore.SIGNAL("pitch(int)"), ((axes[2]*20)))
                        self.emit(QtCore.SIGNAL("roll(int)"), ((axes[3]*-20)))
                        if(self.setpoint != 0):
                            self.emit(QtCore.SIGNAL("throttle(int)"), (((axes[1]*-self.setpoint) + (100-self.setpoint))))
                elif event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN ]:
                    e = event.dict
                    buttons[e['button']] ^= True
                    if(e['button'] == 8 and buttons[e['button']] == True):
                        if(self.setpoint < 100):
                            self.setpoint += 1
                        self.emit(QtCore.SIGNAL("throttle(int)"), (((axes[1]*-self.setpoint) + (100-self.setpoint))))
                    elif(e['button'] == 9 and buttons[e['button']] == True):
                        if(self.setpoint > 2):
                            self.setpoint -= 1
                        self.emit(QtCore.SIGNAL("throttle(int)"), (((axes[1]*-self.setpoint) + (100-self.setpoint))))
                    elif(e['button'] == 12)and buttons[e['button']] == True:
                        if(self.setpoint > 0):
                            self.setpoint = 99
                            self.emit(QtCore.SIGNAL("throttle(int)"), 0)
            time.sleep(0.01)
