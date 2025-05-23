""" When run, this file will connect to the ip_address_server at a static IP and send a json packet with information regarding device """

import socket
import fcntl
import struct
import shutil
import socketio as sio
import subprocess
from time import sleep

from printer_info import IS_PRINTER, HARDWARE_SERIES, HARDWARE_VERSION

USE_NMCLI = shutil.which("nmcli") is not None
SERVER_IP = "nordinip.ee.byu.edu"
# SERVER_PORT is default https port
WAN_IP = "8.8.8.8"  # Google DNS to check connectivity

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

def is_wifi_up(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "2", ip], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def restart_wifi():
    print("Wi-Fi down. Restarting interface...")
    if USE_NMCLI:
        subprocess.call(["sudo", "nmcli", "device", "disconnect", "wlan0"])
        sleep(5)
        subprocess.call(["sudo", "nmcli", "device", "connect", "wlan0"])
    else:
        subprocess.call(["sudo", "ip", "link", "set", "wlan0", "down"])
        sleep(5)
        subprocess.call(["sudo", "ip", "link", "set", "wlan0", "up"])
    sleep(5)  # Give time for reconnect

# Send information to server via socket
socketio = None
while True:
    # Check if Wi-Fi is up and restart if not
    if not is_wifi_up(SERVER_IP) and not is_wifi_up(WAN_IP):
        restart_wifi()

    # Get information about device and pack into dictionary
    hostname = socket.gethostname()
    ip_address = get_ip_address()
    port = 5000
    type = "nordin_printer" if IS_PRINTER else "nordin_device"

    info = {
        "type": type,
        "name": hostname,
        "address": ip_address,
        "port": port,
        "series": HARDWARE_SERIES,
        "version": HARDWARE_VERSION,
    }

    if socketio is not None:
        try:
            socketio.disconnect()
        except Exception:
            pass
    try:
        address = f"https://{SERVER_IP}"
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
    except Exception as e:
        print(f"Unexpected error: {e}")

    sleep(60)  # Wait 1 minute