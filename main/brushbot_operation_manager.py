import machine
import ujson
from main.constants import Constants
from main.leds import LEDs
from main.networking import Networking
from main.ina219 import INA219
from main.tca9548a import TCA9548A
from main.vl6180 import VL6180
from main.drv8836 import DRV8836
from main.timers import Timers

class BrushbotOperationManager:
    def __init__(self):
        # pins
        self.repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        self.en_tca = machine.Pin(13, machine.Pin.OUT)
        self.en_vl = machine.Pin(19, machine.Pin.OUT)
        self.en_motor = machine.Pin(33, machine.Pin.OUT)
        self.I2C = machine.SoftI2C(machine.Pin(22), machine.Pin(21))
        # hardware and software components
        self.leds = None
        self.net = None
        self.ina = None
        self.tca = None
        self.drv = None
        self.timers = None
        # sensor values variables
        self.ina_voltage = 99.9
        self.ina_current = 99.9
        self.ina_power = 99.9
        self.dist_readings = 8*[0]
        # messages
        self.HEARTBEAT_MSG = {
            'id': Constants.MSG_ID_HEARTBEAT,
            'mac': self.net.mac,
            'ip': self.net.ip,
            'port': Constants.PORT
        }
        self.HEARTBEAT_MSG_JSON = ujson.dumps(self.HEARTBEAT_MSG)
        self.SENSOR_MSG = {
            'id': Constants.MSG_ID_SENSORS,
            'inaV': 0.0,
            'inaC': 0.0,
            'inaP': 0.0,
            'ir': 8*[0.0]
        }

    def init_leds(self):
        self.leds = LEDs()
        self.leds.init()

    def init_net(self):
        self.net = Networking()
        self.net.init()

    def init_ina(self):
        try:
            self.ina = INA219(0.05, self.I2C) # shunt resistance = 0.05
            self.ina.configure()
            print('BOM::INA219 successfully configured at address ' + str(self.ina._address))
        except Exception as e:
            print('BOM::INA219 failed to initialize at address ' + str(self.ina._address) + '(Exception: ' + str(e) + ')')

    def init_tca(self):
        self.en_tca.value(1)
        self.tca = TCA9548A(self.I2C)

    def init_vl(self):
        # turn on, test initialization, and turn off
        self.en_vl.value(1)
        for channel in range(8):
            try:
                self.tca.switch_channel(channel)
                vl = VL6180(self.tca.bus)
                print('BOM::VL6180 successfully configured on channel ' + str(channel) + ' at address 0x29')
            except Exception as e:
                print('BOM::VL6180 failed to initialize on channel ' + str(channel) + ' at address 0x29 (Exception: ' + str(e) + ')')
        self.en_vl.value(0)

    def init_drv(self):
        self.en_motor.value(1)
        try:
            self.drv = DRV8836(machine.Pin(14), machine.Pin(25), machine.Pin(26), machine.Pin(27))
            self.drv.stop()
            print('BOM::DRV8836 successfully initialized')
        except Exception as e:
            print('BOM::DRV8836 failed to initialize (Exception: ' + str(e) + ')')

    def init_timers(self):
        self.timers = Timers()

    def initialize(self):
        self.init_leds() # init leds
        self.leds.blink_state_led(n=1, dt=1) # start initialization: blink state led once
        self.init_net() # connect to wifi
        self.init_ina() # init power sensor
        self.init_tca() # init I2C multiplexer
        self.init_vl() # init and test distance sensors
        self.init_drv() # init motor controller
        self.init_timers() # init message and loop timers
        self.leds.blink_state_led(n=2, dt=0.25) # end initialization: blink state led twice

    def repl_handling(self):
        if self.repl_button.value() == 0:
            print('BOM::Dropping to REPL')
            sys.exit()

    def udp_receive(self):
        print('BOM::Receiving udp...')
        udp_msg_json = []
        try:
            udp_msg_json, addr = self.net.socket.recvfrom(256)
        except Exception as e:
            print('BOM::Receiving udp timedout (Exception: ' + str(e) + ')')
        if not udp_msg_json == []:
            udp_msg = ujson.loads(udp_msg_json)
            if udp_msg['id'] == Constants.MSG_ID_MOTORS_CMD:
                v = udp_msg['v']
                self.drv.setLeft(v[1])
                self.drv.setRight(v[0])
                self.timers.reset_motors()
                print('BOM::Received and set motor commands: ' + str(v))
            elif udp_msg['id'] == Constants.MSG_ID_LEDS_CMD:
                led0 = udp_msg['led0']
                led1 = udp_msg['led1']
                self.leds.led_neopixel[0] = tuple(led0)
                self.leds.led_neopixel[1] = tuple(led1)
                self.leds.led_neopixel.write()
                self.timers.reset_leds()
                print('BOM::Received and set led commands: ' + str(led0) + ', ' + str(led1))
            elif udp_msg['id'] == MSG_ID_SENSORS_ON:
                self.en_vl.value(1)
                print('BOM::Received command to turn on sensors')
            elif udp_msg['id'] == MSG_ID_SENSORS_OFF:
                self.en_vl.value(0)
                print('BOM::Received command to turn off sensors')

    def udp_send(self):
        # heartbeat
        if self.timers.heartbeat_timedout():
            try:
                self.net.socket.sendto(self.HEARTBEAT_MSG_JSON, (Constants.IP_MANAGER, Constants.PORT))
                print('BOM::Sent heartbeat message ' + str(self.HEARTBEAT_MSG_JSON))
            except Exception as e:
                print('BOM::Failed to send heartbeat message ' + str(self.HEARTBEAT_MSG_JSON))
            self.timers.reset_heartbeat()
        # sensors
        if self.timers.sensors_timedout():
            # power sensor readings
            try:
                self.ina_voltage = self.ina.voltage()
                self.ina_current = self.ina.current()
                self.ina_power = self.ina.power()
            except Exception as e:
                self.ina_voltage = 99.9
                self.ina_current = 99.9
                self.ina_power = 99.9
                print('BOM::INA219 sensor is malfunctioning (Exception: ' + str(e) + ')')
            # distance sensor readings
            self.dist_readings = 8*[0]
            if self.en_vl.value() == 1:
                for channel in range(8):
                    try:
                        self.tca.switch_channel(channel)
                        vl = VL6180(self.tca.bus)
                        self.dist_readings[channel] = vl.range()*0.1/255.0
                        print('BOM::VL6180 on channel ' + str(channel) + ' reading: ' + str(self.dist_readings[channel]))
                    except Exception as e:
                        print('BOM::VL6180 on channel ' + str(channel) + ' doesn''t work (Exception: ' + str(e) + ')')
            else:
                print('BOM::VL6180 are switched off')
            sensor_msg = self.SENSOR_MSG
            sensor_msg['inaV'] = self.ina_voltage
            sensor_msg['inaC'] = self.ina_current
            sensor_msg['inaP'] = self.ina_power
            sensor_msg['ir'] = self.dist_readings
            sensor_msg_json = ujson.dumps(sensor_msg)
            try:
                self.net.socket.sendto(sensor_msg_json, (Constants.IP_MANAGER, Constants.PORT))
                print('BOM::Sent sensors message ' + str(sensor_msg_json))
            except Exception as e:
                print('BOM::Failed to send sensors message ' + str(sensor_msg_json))
            self.timers.reset_sensors()

    def timeout_handling(self):
        if self.timers.motors_timedout():
            self.drv.stop()
            # print('BOM::Motors message timeout, stopped motors')
        if self.timers.leds_timedout():
            self.leds.led_neopixel[0] = tuple([0]*3)
            self.leds.led_neopixel[1] = tuple([0]*3)
            self.leds.led_neopixel.write()
            # print('BOM::LEDs message timeout, turned off leds')

    def battery_indicator_led(self):
        self.leds.battery_indicator(self.ina_voltage)

    def loop_time_control(self):
        self.timers.loop_sleep()

    def run(self):
        self.timers.reset()
        while True:
            self.timers.reset_loop() # reset loop time
            self.repl_handling() # handle REPL button
            self.udp_receive() # receive and process messages via udp
            self.udp_send() # send heartbeat and sensor messages via udp
            self.timeout_handling() # motors and leds commands timeout
            self.battery_indicator_led() # show battery level through state led blink
            self.loop_time_control() # limit min loop time
