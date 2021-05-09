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

    def get_buttons(self):
        """
        Get all the buttons state.

        Return:
            A tuple containing all the buttons state. 1 is pressed, 0 is depressed.
        """
        self._logger.debug(f"reading all button state of controller {self.get_name()}")
        button_count = self._joystick.get_numbuttons()
        button_states = [int(self._joystick.get_button(i)) for i in range(button_count)]

        self._logger.debug(f"button states: {button_states}")

        return (button_states)

    def get_axis(self):
        """
        Get all axis position.

        Return:
            A tuple containing all the axis positions. The positions are ranging from -1 to 1.
        """
        self._logger.debug(f"reading all axis positions of controller {self.get_name()}")
        axis_count = self._joystick.get_numaxes()
        axis_positions = [float(self._joystick.get_axis(i)) for i in range(axis_count)]
        axis_positions = [round(pos, self._ndigit) for pos in axis_positions]

        self._logger.debug(f"axis positions: {axis_positions}")

        return (axis_positions)

    def quit(self):
        """
        Uninitialize the controller.
        """
        self._logger.info(f"unitializing controller")
        self._joystick.quit()
