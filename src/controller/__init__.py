import json
import logging
import os

import pygame

class Controller:
    """
    Class implementing the controller function.
    """
    CONFIG_ROOT_DIR = './src/controller/configs/'
    CTRL_FRAME_RATE = 10

    def __init__(self, idx, name, app, ndigit=2):
        """
        Constructor.

        Params:
            idx:        The index of the controller from 0 to pygame.joystick.get_count().
            name:       The controller name.
            app:        The app instances for generating events.
            ndigit:     The digit number for the axis precision. Default: 2.
        """
        self._logger = logging.getLogger(f"CTRL_{idx}")
        self._logger.debug(f"creating controller {name}")
        self._joystick = pygame.joystick.Joystick(idx)
        self._joystick.init()

        self._idx = idx
        self._ndigit = ndigit
        self._app = app

        file_name = f"{name.lower().replace(' ', '_')}.json"
        config_file = os.path.join(self.CONFIG_ROOT_DIR, file_name)
        with open(config_file) as raw_config:
            self._config = json.load(raw_config)

    @classmethod
    def list_connected(cls):
        """
        List the connected and supported controller.

        Return:
            A Dictionary listing the connected and supported controller.
            The keys is the controller name and the value is its index.
        """
        logger = logging.getLogger('CTRL_CLS')
        logger.debug('listing connected/supported controller')
        connected = []
        for id in range(pygame.joystick.get_count()):
            controller_name = pygame.joystick.Joystick(id).get_name()
            connected.append(controller_name)

        supported = [f.replace('.json', '') for f in os.listdir(cls.CONFIG_ROOT_DIR)]
        connected_supported = {}
        for idx in range(len(connected)):
            if any(connected[idx].lower().replace(' ', '_') in ctrl_name for ctrl_name in supported):
                connected_supported[connected[idx]] = idx

        logger.debug(f"found the following controllers: {connected_supported}")

        return connected_supported

    def get_name(self):
        """
        Get the joystick name.

        Return:
            The name of the controller.
        """
        return self._joystick.get_name()

    def get_idx(self):
        """
        Get the joystick index
        Return:
            The index of the controller.
        """
        return self._idx

    def get_type(self):
        """
        Get the controller type.

        Return:
            The controller type.
        """
        return self._config['type']

    def get_funct_map(self):
        """
        Get the controller function mapping.

        Return:
            A dictionary containing the map of the functions.
        """
        return self._config['mapping']

    def get_axis_map(self):
        """
        Get the controller axis mapping.

        Return:
            The list containing the map of the axis.
        """
        return self._config['controls']['axis']

    def get_buttons_map(self):
        """
        Get the controller buttons mapping.

        Return:
            The list containing the map of the buttons.
        """
        return self._config['controls']['buttons']

    def get_hats_map(self):
        """
        Get the controller hats mapping.

        Return:
            The list containing the map of the hats.
        """
        return self._config['controls']['hats']

    def quit(self):
        """
        Uninitialize the controller.
        """
        self._logger.info(f"unitializing controller")
        self._joystick.quit()
