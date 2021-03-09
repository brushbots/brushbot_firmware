import machine
import ustruct


class TCA9548A():
    def __init__(self, i2c_interface, address=0x70):
        self.address = address
        self.bus = i2c_interface

    def switch_channel(self,channel):
        self.bus.writeto(self.address, ustruct.pack('B',1 << channel))
