import pygame

from logger import initLogger
from pkgs.joystick import Joystick
import pkgs.mqttClient as client

from pkgs.ui import AppComposer

# App constants
_CLIENT_ID = 'commander'
_CLIENT_PASSWD = '12345'
_CTRL_FRAME_RATE = 10

# App data
_globalLogger: object = None
_logger: object = None
_ui: object = None
_units = {'active': None, 'list': []}


def main():
    """
    Application main.
    """
    logger = initLogger()
    app = AppComposer(logger)
    app.run()


if __name__ == '__main__':
    main()
