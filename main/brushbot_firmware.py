import utime
from machine import Pin

def run():
    led = Pin(32, Pin.OUT)
    while True:
        led.value(1)
        utime.sleep(0.5)
        led.value(0)
        utime.sleep(0.5)
