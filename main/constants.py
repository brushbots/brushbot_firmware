class Constants:
    # networking
    IP_MANAGER = '192.168.139.1'
    IP_SUBNET = '255.255.255.0'
    IP_GATEWAY = '192.168.139.26'
    IP_BROADCAST = '192.168.139.255'
    IP_DNS = '8.8.8.8'
    IP_ROBOTS = [
        '192.168.139.101',
        '192.168.139.102'
        ]
    MAC_ROBOTS = [
        '98:f4:ab:1d:d5:e4',
        '98:f4:ab:1d:d5:e5' # made up
        ]
    UDP_PORT = 49152
    # communication
    MSG_ID_HEARTBEAT = 0
    MSG_ID_MOTORS_CMD = 1
    MSG_ID_LEDS_CMD = 2
    MSG_ID_SENSORS_ON = 3
    MSG_ID_SENSORS_OFF = 4
    MSG_ID_SENSORS = 5
