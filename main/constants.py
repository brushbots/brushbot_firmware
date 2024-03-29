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
        '192.168.0.110',
        '192.168.0.111',
        '192.168.0.112',
        '192.168.0.113',
        '192.168.0.114',
        '192.168.0.115',
        '192.168.0.116',
        '192.168.0.118',
        '192.168.0.119',
        '192.168.0.120',
        '192.168.0.121'
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
        '98:f4:ab:1d:d5:d8',
        '98:f4:ab:1d:d6:94',
        '98:f4:ab:1d:d6:48',
        '98:f4:ab:1d:d6:c8',
        '98:f4:ab:1d:d6:d8',
        '98:f4:ab:1d:d5:ec',
        '98:f4:ab:1d:d5:d0',
        '98:f4:ab:1d:d6:3c',
        '98:f4:ab:1d:d5:e4',
        '98:f4:ab:1d:d6:2c',
        '98:f4:ab:1d:d6:04'
        ]
    UDP_PORT = 49152

    # communication
    MSG_ID_HEARTBEAT = 0
    MSG_ID_MOTORS_CMD = 1
    MSG_ID_LEDS_CMD = 2
    MSG_ID_SENSORS_ON = 3
    MSG_ID_SENSORS_OFF = 4
    MSG_ID_SENSORS = 5

    # timeouts
    TIMEOUT_LOOP = 20
    TIMEOUT_HEARTBEAT = 2000
    TIMEOUT_MOTORS = 1000
    TIMEOUT_LEDS = 1000
    TIMEOUT_SENSORS = 100

    # battery led indicator
    V_BATT_THRESH = [3.2, 3.5]
    DT = [500, 2000]
