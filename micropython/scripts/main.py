import machine
import neopixel
import sys
import utime
import vl6180
import DRV8836
import networking
from ina219 import INA219
import tca9548a
import ujson
import random
from constants import Constants

DEBUG = False

############    Initiazation Settings - Don't Change    ######################
if DEBUG:
    print('\n\n\nInitializing devices, the red LED on the robot should light up in a moment\n\n\n')

# connections
try:
    networking.connect()
    sock_pc2bb, sock_bb2pc = networking.connect_socket()
except:
    if DEBUG:
        print('\n\n\nConnection failed\n\n\n')

# Default Reset Pin Definition. Don't Change.
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)

# Default LED pin. Bot Running Indicator. This LED is right to the left of the ESP board.
led = machine.Pin(32, machine.Pin.OUT)
led.value(0)
utime.sleep(0.5)
led.value(1)
utime.sleep(0.5)
led.value(0)

# Sensor-enable Initialization
sensor_en = machine.Pin(19, machine.Pin.OUT)
sensor_en.value(1)
mux_en = machine.Pin(13, machine.Pin.OUT)
mux_en.value(1)

# I2C interface
i2c_interface = machine.I2C(-1, machine.Pin(22), machine.Pin(21))

# LED neoPixel on Pin 37 setup
try:
    neoPixel = neopixel.NeoPixel(machine.Pin(23), 2)
    if DEBUG:
        print('\n\n\nSuccessfully configured neoPixels\n\n\n')
except:
    if DEBUG:
        print('\n\n\nFailed to configure neoPixels\n\n\n')

# I2C Multiplexer Initiazation
# tca = tca9548a.TCA9548A(0x70)
tca = tca9548a.TCA9548A(i2c_interface)

# Laser Sensor Initialization
for channel in range(8):
    try:
        tca.switch_channel(channel)
        sensor = vl6180.Sensor(tca.bus)
        if DEBUG:
            print('\n\n\nSuccessfully configured VL6180x sensor on channel ' + str(channel) + ' at address 0x29\n\n\n')
    except Exception as e:
        if DEBUG:
            print('\n\n\nFailed to initialize VL6180x sensor on on channel ' + str(channel) + ' at address 0x29\n\n\n')
            print('=========\n=========\n=========')
            print('Exception')
            print(e)
            print('=========\n=========\n=========')
            print('\n\n\n')

# Current Sensor Initialization
shunt_resistance = 0.05 # Change if needed
try:
    ina = INA219(shunt_resistance, i2c_interface)
    ina.configure()
    if DEBUG:
        print('\n\n\nSuccessfully configured INA219 sensor at address ' + str(ina._address))
except:
    if DEBUG:
        print('\n\n\nFailed to initialize INA219 sensor at address ' + str(ina._address) + '\n\n\n')

# Motor Driver Initialization
try:
    drv = DRV8836.DRV8836(machine.Pin(14), machine.Pin(25),
                          machine.Pin(26), machine.Pin(27))
    drv.stop()
    motor_en = machine.Pin(33, machine.Pin.OUT)
    motor_en.value(1)
except Exception as e:
    if DEBUG:
        print('\n\n\nFailed to initialize DRV8836\n\n\n')

utime.sleep(1)

# Default LED pin. Bot Running Indicator. This LED is right to the left of the ESP board.
led.value(1)
####################    End of Initialization   ################################

ir_readings = 8*[0];
ina_voltage = 0
ina_current = 0
ina_power = 0

last_sent_mac_ip_port = utime.ticks_ms()
last_read_sensors = utime.ticks_ms()
last_received_motor_commands = utime.ticks_ms()
last_received_led_commands = utime.ticks_ms()
last_sent_sensors = utime.ticks_ms()

while True:
    loop_start_time = utime.ticks_ms()

    # If button 0 is pressed, drop to REPL
    if repl_button.value() == 0:
        if DEBUG:
            print('\n\n\nDropping to REPL\n\n\n')
        sys.exit()

    # SEND MAC IP PORT TO SERVER
    if DEBUG:
        print('\n\n\nSending mac ip port\n\n\n')
    if utime.ticks_diff(utime.ticks_ms(), last_sent_mac_ip_port) > 2000:
        msg_dict = {
            'id': Constants.ID_MAC_IP_PORT,
            'mac': '4c:11:ae:b5:01:90',
            'ip': Constants.ROBOT_IP,
            'port': Constants.PORT_HEARTBEAT
        }
        sock_pc2bb.sendto(ujson.dumps(msg_dict), (Constants.SERVER_IP, Constants.PORT_HEARTBEAT)) # sock_pc2bb on port 1846 remote
        last_sent_mac_ip_port = utime.ticks_ms()

    # READ SENSORS
    if DEBUG:
        print('\n\n\nGetting sensors\n\n\n')
    # distance sensors
    if utime.ticks_diff(utime.ticks_ms(), last_read_sensors) > 100: # read sensors at <10Hz
        for channel in range(8):
           try:
               tca.switch_channel(channel)
               sensor = vl6180.Sensor(tca.bus)
               ir_readings[channel] = sensor.range()*0.1/255.0
               if DEBUG:
                   print('\n\n\nSensor on channel ' + str(channel) + ' reading: ' + str(ir_readings[channel]) + '\n\n\n')
           except Exception as e:
               if DEBUG:
                   print('\n\n\nSensor on channel ' + str(channel) + ' doesn''t work\n\n\n')
                   print('=========\n=========\n=========')
                   print('Exception')
                   print(e)
                   print('=========\n=========\n=========')
                   print('\n\n\n')
        last_read_sensors = utime.ticks_ms()
    # current-voltage-power sensor
    ina_voltage = ina.voltage()
    ina_current = ina.current()
    ina_power = ina.power()
    try:
        data = "Bus Voltage: %.3f" % ina_voltage + "  |  Current: %.3f mA" % ina_current + "  |  Power: %.3f mW" % ina_power
        if DEBUG:
            print('\n\n\n' + data + '\n\n\n')
    except:
        if DEBUG:
            print('\n\n\nINA219 sensor is malfunctioning\n\n\n')

    # RECEIVE ACTUATORS FROM SERVER
    if DEBUG:
        print('\n\n\nReading actuators\n\n\n')
    recv_data = []
    try:
        recv_data, addr = sock_pc2bb.recvfrom(256)
    except:
        if DEBUG:
            print('\n\n\nTimedout\n\n\n')
    if not recv_data == []:
        msg_dict = ujson.loads(recv_data)
        if msg_dict['id'] == Constants.ID_MOTOR_COMMAND: # motor commands
            v = msg_dict['v']
            last_received_motor_commands = utime.ticks_ms()
            if DEBUG:
                print('\n\n\nReceived motor commands: ' + str(v) + '\n\n\n')
        elif msg_dict['id'] == Constants.ID_LED_COMMAND: # led commands
            led0 = msg_dict['led0']
            led1 = msg_dict['led1']
            last_received_led_commands = utime.ticks_ms()
            if DEBUG:
                print('\n\n\nReceived led commands: ' + str(led0) + ', ' + str(led1) + '\n\n\n')

    # SET ACTUATORS
    if DEBUG:
        print('\n\n\nSetting actuators\n\n\n')
    if not recv_data == []:
        if msg_dict['id'] == Constants.ID_MOTOR_COMMAND: # motor commands
            drv.setLeft(v[1])
            drv.setRight(v[0])
        elif msg_dict['id'] == Constants.ID_LED_COMMAND: # led commands
            neoPixel[0] = tuple(led0)
            neoPixel[1] = tuple(led1)
            neoPixel.write()
    if utime.ticks_diff(utime.ticks_ms(), last_received_motor_commands) > 500: # 0.5s timeout for motor commands
        drv.setLeft(0)
        drv.setRight(0)
        # drv.stop()
    if utime.ticks_diff(utime.ticks_ms(), last_received_led_commands) > 5000: # 5s timeout for led commands
        neoPixel[0] = tuple([0]*3)
        neoPixel[1] = tuple([0]*3)
        neoPixel.write()

    # SEND SENSORS TO SERVER
    if DEBUG:
        print('\n\n\nSending sensors\n\n\n')
    if utime.ticks_diff(utime.ticks_ms(), last_sent_sensors) > 100: # send sensors at <10Hz
        msg_dict = {
            'id': Constants.ID_SENSORS,
            'inaV': ina_voltage,
            'inaC': ina_current,
            'inaP': ina_power,
            'ir': ir_readings
        }
        sock_pc2bb.sendto(ujson.dumps(msg_dict), (Constants.SERVER_IP, Constants.PORT_SENSORS)) # sock_pc2bb on port 1847 remote
        last_sent_sensors = utime.ticks_ms()
        if DEBUG:
            print('\n\n\nSend sensor readings: ' + str(ir_readings) + '\n\n\n')

    loop_duration = utime.ticks_diff(utime.ticks_ms(), loop_start_time)
    if loop_duration < 20:
        utime.sleep_ms(20-loop_duration) # run at <50Hz

sock_pc2bb.close()
sock_bb2pc.close()
