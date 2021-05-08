import sys
import logging

from controller import Controller
from client import Client

class App:
    """
    The application base class.
    """

    def __init__(self):
        """
        Constructor.
        """
        logging.basicConfig(level=logging.DEBUG)
        logging.info('launcihing application...')

        logging.info('initializing mqtt client.')
        self._client = Client('12345')
        logging.info('mqtt client initialized.')

        logging.info('initializing controller.')
        controllers = Controller.list_connected()
        logging.debug(f"controller list: {controllers}")
        self._driving_wheel = Controller(0, controllers[0], self._client)
        logging.info('controller initialzed.')

        logging.info('application launched.')

    def quit(self):
        """
        Quit the application.
        """
        logging.info('quitting the application')
        self._client.disconnect()
        sys.exit()

    def loop(self):
        """
        The application loop.
        """
        while True:
            self._driving_wheel.process_events()

if __name__ == '__main__':
    app = App()
    app.loop()
