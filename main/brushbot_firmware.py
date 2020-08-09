import utime
from machine import Pin

def run_main():
    led = Pin(32, Pin.OUT)
    while True:
        led.value(1)
        utime.sleep(0.25)
        led.value(0)
        utime.sleep(0.25)
