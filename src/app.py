import sys
import logging

import pygame

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

        logging.info('initializing pygame.')
        pygame.init()
        logging.info('pygame initialized.')

        logging.info('initializing controller.')
        controllers = Controller.list_connected()
        self._driving_wheel = Controller(0, controllers[0])
        logging.info('controller initialzed.')

        logging.info('initializing mqtt client.')
        self._client = Client('12345')
        logging.info('mqtt client initialized.')

        logging.info('initializing application window')
        self._screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
        self._clock = pygame.time.Clock()
        logging.info('apllication window initialized.')

        logging.info('application launched.')

    def quit(self):
        """
        Quit the application.
        """
        logging.info('quitting the application')
        self._client.disconnect()
        pygame.quit()
        sys.exit()

    def process_pygame_events(self):
        """
        Process the pygame events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.update()

    def process_controller(self):
        """
        Process the controller data.
        """
        button_states = self._driving_wheel.get_buttons()
        axis_positions = self._driving_wheel.get_axis()

    def game_loop(self):
        """
        The application game loop.
        """
        while True:
            self.process_pygame_events()
            self.process_controller()

            # Redraw
            pygame.display.flip()
            self._clock.tick(120)

if __name__ == '__main__':
    app = App()
    app.game_loop()
