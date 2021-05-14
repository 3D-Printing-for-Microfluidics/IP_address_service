from os import name
import socket
from time import sleep
import time


class DeviceTables:
    def __init__(self):
        self.printers = {}
        self.devices = {}
        self.timestamps = {}

    def register_ip(message):
        type = message["type"]
        name = message["name"]
        address = message["address"]
        port = message["port"]
        series = message["series"]
        version = message["version"]

        if "nordin" in type:
            # add printers to dictionary
            printerInfo = {
                "address": address,
                "stat": -1,
                "port": port,
                "series": series,
                "version": version,
            }

            self.timestamps[name] = time.time()
            if type == b"nordin_printer":
                self.printers[name] = printerInfo
                print("PRINTER: {}: {} at {}".format(name, address))
            elif type == b"nordin_device":
                self.devices[name] = printerInfo
                print("DEVICE: {}: {} at {}".format(name, address))
            else:
                print("NOT ADDED: {}: {} at {}".format(name, address))

    def clear_all_ip_addresses(self):
        self.printers.clear()
        self.devices.clear()
        self.timestamps.clear()

    def unregister_ip_address(self, hostname):
        # try removing as printer
        try:
            del self.printers[hostname]
        except KeyError:
            pass
        # else try removing as device
        try:
            del self.devices[hostname]
        except KeyError:
            pass
        del self.timestamps[name]
        print("Removed: {}".format(hostname))

    def check_all_printer_status(self):
        for printer in list(self.printers):
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(2)
            rpi_port = (self.printers[printer]["address"], 22)
            rpi_up = a_socket.connect_ex(rpi_port)
            a_socket.close()

            if rpi_up == 0:
                # print("Port is open")
                a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                a_socket.settimeout(2)
                server_port = (
                    self.printers[printer]["address"],
                    self.printers[printer]["port"],
                )
                server_up = a_socket.connect_ex(server_port)
                a_socket.close()

                if server_up == 0:
                    # print("Server is up")
                    self.printers[printer]["stat"] = 2
                else:
                    # print("Server is down")
                    self.printers[printer]["stat"] = 1
            else:
                # print("Port is not open")
                self.printers[printer]["stat"] = 0

    def check_all_device_status(self):
        for device in list(self.devices):
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(2)
            rpi_port = (self.devices[device]["address"], 22)
            rpi_up = a_socket.connect_ex(rpi_port)
            a_socket.close()

            if rpi_up == 0:
                # print("Server is up")
                self.devices[device]["stat"] = 2
            else:
                # print("Port is not open")
                self.devices[device]["stat"] = 0

    def loop(self):
        try:
            while True:
                currentTime = time.time()
                for name in list(self.timestamps):
                    lastTime = self.timestamps[name]
                    if currentTime - lastTime > 86400:
                        self.unregister_ip_address(name)
                sleep(600)

        except KeyboardInterrupt:
            pass
        finally:
            self.clear_all_ip_addresses()
