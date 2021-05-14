""" When run, this file will connect to the ip_address_server at a static IP and send a json packet with information regarding device """

import socket
import fcntl
import struct
import socketio as sio
from time import sleep

from printer_info import IS_PRINTER, HARDWARE_SERIES, HARDWARE_VERSION

SERVER_IP = "10.37.22.47"
SERVER_PORT = "5000"


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            return socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915, struct.pack("256s", b"wlan0"))[20:24]
            )
        except OSError:
            sleep(1)


hostname = socket.gethostname()
ip_address = get_ip_address()
port = None
type = ""

if IS_PRINTER:
    type = "nordin_printer"
    port = 5000
else:
    type = "nordin_device"

info = {
    "type": type,
    "name": hostname,
    "address": ip_address,
    "port": port,
    "series": HARDWARE_SERIES,
    "version": HARDWARE_VERSION,
}

try:
    socket = sio.Client()
    socket.connect("https://{}:{}".format(SERVER_IP, SERVER_PORT), namespaces=["/"])

    socket.emit("register_ip", info, namespace="/")

    sleep(2)

    socket.disconnect()

except sio.exceptions.ConnectionError:
    pass
