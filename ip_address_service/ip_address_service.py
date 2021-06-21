""" When run, this file will connect to the ip_address_server at a static IP and send a json packet with information regarding device """

import socket
import fcntl
import struct
import socketio as sio
from time import sleep

from printer_info import IS_PRINTER, HARDWARE_SERIES, HARDWARE_VERSION

SERVER_IP = "nordinip.ee.byu.edu"
# SERVER_PORT is default https port

"""
Get my ip address for wireless interface using socket
"""


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            return socket.inet_ntoa(
                fcntl.ioctl(s.fileno(), 0x8915, struct.pack("256s", b"wlan0"))[20:24]
            )
        except OSError:
            sleep(1)


# Send information to server via socket
socketio = None
while True:

    # Get information about device and pack into dictionary
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
        address = "https://{}".format(SERVER_IP)
        # socketio = sio.Client(request_timeout=30, ssl_verify=False)
        socketio = sio.Client(request_timeout=30)
        socketio.connect(address, namespaces=["/"])

        # If the server's data was flushed, send it again
        @socketio.on("flush", namespace="/")
        def flush():
            print("Flushed - Sending message")
            socketio.emit("register_ip", info, namespace="/")

        # print("Sending message")
        socketio.emit("register_ip", info, namespace="/")

    except sio.exceptions.ConnectionError:
        print("Connection failed")

    # Wait 10 minutes
    sleep(600)

    socketio.disconnect()
