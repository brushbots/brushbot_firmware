class Constants:
    # networking
    IP_MANAGER = '192.168.0.2'
    IP_SUBNET = '255.255.255.0'
    IP_GATEWAY = '192.168.0.1'
    IP_BROADCAST = '192.168.0.255'
    IP_DNS = '8.8.8.8'
    IP_ROBOTS = [
        '192.168.0.101',
        '192.168.0.102',
        '192.168.0.103',
        '192.168.0.104',
        '192.168.0.105',
        '192.168.0.106',
        '192.168.0.107',
        '192.168.0.108',
        '192.168.0.109',
        '192.168.0.119'
        ]
    MAC_ROBOTS = [
        '98:f4:ab:1d:d5:cc',
        '98:f4:ab:1d:d6:40',
        '98:f4:ab:1d:d6:08',
        '98:f4:ab:1d:d5:c0',
        '98:f4:ab:1d:d5:f8',
        '98:f4:ab:1d:d6:00',
        '98:f4:ab:1d:d5:fc',
        '98:f4:ab:1d:d5:dc',
        '98:f4:ab:1d:d6:68',
        '98:f4:ab:1d:d5:e4'
        ]
    UDP_PORT = 49152
    # communication
    MSG_ID_HEARTBEAT = 0
    MSG_ID_MOTORS_CMD = 1
    MSG_ID_LEDS_CMD = 2
    MSG_ID_SENSORS_ON = 3
    MSG_ID_SENSORS_OFF = 4
    MSG_ID_SENSORS = 5
