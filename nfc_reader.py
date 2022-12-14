import evdev
from evdev import ecodes
import json
from datetime import datetime
from socket import *

from response_handler import ResponseHandler

serverName = '255.255.255.255'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

response_handler = ResponseHandler()


class Device:

    name = 'Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader'

    @classmethod
    def list(cls, show_all=False):
        # list the available devices
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if show_all:
            for device in devices:
                print("event: " + device.fn, "name: " + device.name, "hardware: " + device.phys)
        return devices

    @classmethod
    def connect(cls):
        # connect to device if available
        try:
            device = [dev for dev in cls.list() if cls.name in dev.name][0]
            device = evdev.InputDevice(device.fn)
            return device
        except IndexError:
            print(
                "Device not found.\n - Check if it is properly connected. \n - Check permission of /dev/input/ (see README.md)")
            exit()


    @classmethod
    def run(cls):
        device = cls.connect()
        container = []
        try:
            device.grab()
            print("RFID scanner is ready....")
            print("Press Control + c to quit.")
            for event in device.read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    digit = evdev.ecodes.KEY[event.code]
                    if digit == 'KEY_ENTER':
                        tag = "".join(i.strip('KEY_') for i in container)
                        message = {"nfcCardId": str(tag), "Date": str(datetime.now())}
                        response_handler.show_loading()
                        clientSocket.sendto(json.dumps(message).encode(), (serverName, serverPort))
                        modified_message, server_address = clientSocket.recvfrom(2048)
                        response = modified_message.decode()

                        response_handler.handle_response(response)

                        container = []
                    else:
                        container.append(digit)
        except KeyboardInterrupt:
            # catch all exceptions to be able to release the device
            device.ungrab()
            print('Quitting.')


Device.run()
d