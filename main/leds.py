import machine
import neopixel
import utime
from main.constants import Constants

class LEDs:
    def __init__(self):
        self.led_state = None
        self.led_neopixel = None
        self.led_state_battery = 0
        self.last_blink = utime.ticks_ms()

    def init(self):
        self.led_state = machine.Pin(32, machine.Pin.OUT)
        try:
            self.led_neopixel = neopixel.NeoPixel(machine.Pin(23), 2)
            print('LEDs::Successfully configured neopixels')
        except:
            print('LEDs::Failed to configure neopixels')

    def blink_state_led(self, n=1, dt=1):
        for i in range(n):
            self.led_state.value(0)
            utime.sleep(dt/2.0)
            self.led_state.value(1)
            utime.sleep(dt/2.0)
        self.led_state.value(0)

    def battery_indicator(self, v):
        try:
            dt = Constants.DT[[v<vi for vi in Constants.V_BATT_THRESH].index(True)]
            if utime.ticks_diff(utime.ticks_ms(), self.last_blink) > dt:
                self.led_state_battery = 1 - self.led_state_battery
                self.last_blink = utime.ticks_ms()
            self.led_state.value(self.led_state_battery)
        except:
            self.led_state.value(1)
