import time
__author__ = 'janco'


class PwmBoard:
    #registers
    __MODE1              = 0x00
    __MODE2              = 0x01
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALL_LED_ON_L       = 0xFA
    __ALL_LED_ON_H       = 0xFB
    __ALL_LED_OFF_L      = 0xFC
    __ALL_LED_OFF_H      = 0xFD

    # Bits
    __RESTART            = 0x80
    __SLEEP              = 0x10
    __ALLCALL            = 0x01
    __INVRT              = 0x10
    __OUTDRV             = 0x04

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.write8(self.__MODE2, self.__OUTDRV)
        self.write8(self.__MODE1, self.__ALLCALL)
        time.sleep(0.005)

        mode1 = self.readU8(self.__MODE1)
        mode1 = mode1 & ~self.__SLEEP                           # wake up (reset sleep)
        self.write8(self.__MODE1, mode1)
        time.sleep(0.005)                                       # wait for oscillator

    def setPWM(self, channel, on, off):
        self.write8(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.write8(self.__LED0_ON_H+4*channel, on >> 8)
        self.write8(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.write8(self.__LED0_OFF_H+4*channel, off >> 8)

    def write8(self,reg,value):
        self.bus.write_byte_data(self.address, reg, value)

    def readU8(self,reg):
        return self.bus.read_byte_data(self.address, reg)
