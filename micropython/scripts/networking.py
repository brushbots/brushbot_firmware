import network
import socket
from constants import Constants


def connect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('\n\n\nWIFI --- connecting ...\n\n\n')
        wlan.active(True)
        wlan.ifconfig((Constants.ROBOT_IP,'255.255.255.0',Constants.GATEWAY_IP,'8.8.8.8'))
        wlan.connect('brushbotarium', 'brushy1846')
        while not wlan.isconnected():
            pass
    print('\n\n\nWIFI --- connected\n\n\n')
    return wlan


def connect_socket():
    sock_pc2bb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_bb2pc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('\n\n\nSOCKET --- connecting to %s inbound port %s\n\n\n' % (Constants.ROBOT_IP, Constants.PORT_HEARTBEAT)) # 1846 local
    print('\n\n\nSOCKET --- connecting to %s inbound port %s\n\n\n' % (Constants.ROBOT_IP, Constants.PORT_LOG))
    sock_pc2bb.bind((Constants.ROBOT_IP, Constants.PORT_HEARTBEAT))
    sock_bb2pc.bind((Constants.ROBOT_IP, Constants.PORT_LOG))
    sock_pc2bb.settimeout(1)
    sock_bb2pc.settimeout(1)
    print('\n\n\nSOCKET --- connected\n\n\n')
    return sock_pc2bb, sock_bb2pc
