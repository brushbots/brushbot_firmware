import utime

class Timers:
    def __init__(self):
        self.TIMEOUT_LOOP = 20
        self.TIMEOUT_HEARTBEAT = 2000
        self.TIMEOUT_MOTORS = 1000
        self.TIMEOUT_LEDS = 1000
        self.TIMEOUT_SENSORS = 100
        self.last_loop_start = None
        self.last_heartbeat = None
        self.last_motors = None
        self.last_leds = None
        self.last_sensors = None

    def reset(self):
        self.reset_loop()
        self.reset_heartbeat()
        self.reset_motors()
        self.reset_leds()
        self.reset_sensors()

    def reset_loop(self):
        self.last_loop_start = utime.ticks_ms()

    def reset_heartbeat(self):
        self.last_heartbeat = utime.ticks_ms()

    def reset_motors(self):
        self.last_motors = utime.ticks_ms()

    def reset_leds(self):
        self.last_leds = utime.ticks_ms()

    def reset_sensors(self):
        self.last_sensors = utime.ticks_ms()

    def loop_sleep(self):
        loop_duration = utime.ticks_diff(utime.ticks_ms(), self.last_loop_start)
        if loop_duration < self.TIMEOUT_LOOP:
            utime.sleep_ms(self.TIMEOUT_LOOP-loop_duration)

    def heartbeat_timedout(self):
        return bool(utime.ticks_diff(utime.ticks_ms(), self.last_heartbeat) > self.TIMEOUT_HEARTBEAT)

    def motors_timedout(self):
        return bool(utime.ticks_diff(utime.ticks_ms(), self.last_motors) > self.TIMEOUT_MOTORS)

    def leds_timedout(self):
        return bool(utime.ticks_diff(utime.ticks_ms(), self.last_leds) > self.TIMEOUT_LEDS)

    def sensors_timedout(self):
        return bool(utime.ticks_diff(utime.ticks_ms(), self.last_sensors) > self.TIMEOUT_SENSORS)
