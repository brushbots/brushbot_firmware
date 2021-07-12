import network
import socket
import main.secrets as secrets
from main.constants import Constants

class Networking:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.mac = None
        self.ip = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connect_wifi(self):
        print('WiFi::Connecting...')
        self.wlan.active(True)
        self.mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*(self.wlan.config('mac')))
        print('WiFi::MAC address ' + self.mac)
        self.ip = Constants.IP_ROBOTS[Constants.MAC_ROBOTS.index(self.mac)]
        self.wlan.ifconfig((self.ip,Constants.IP_SUBNET,Constants.IP_GATEWAY,Constants.IP_DNS))
        self.wlan.connect(secrets.NETWORK_SSID, secrets.NETWORK_PWD)
        while not self.wlan.isconnected():
            pass
        print('WiFi::Connected with ip ' + self.ip)
        print('WiFi::Network config:', self.wlan.ifconfig())

    def init_socket(self):
        print('Socket::Binding socket on %s to port %s' % (self.ip, Constants.PORT))
        self.socket.bind((self.ip, Constants.PORT))
        self.socket.settimeout(1)
        print('Socket::Done')

    def init(self):
        self.connect_wifi()
        self.init_socket()
