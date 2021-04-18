import json
import logging
import os
import pygame

def list_controller():
    """
    List the connected controller.
    """

class Controller:
    """
    Class implementing the controller function.
    """

    CONFIG_ROOT_DIR = './src/controller/configs/'

    def __init__(self, id, name, ndigit=2):
        """
        Constructor.

        Params:
            id:         The ID of the controller from 0 to pygame.joystick.get_count().
            name:       The controller name.
            ndigit:     The digit number for the axis precision. Default: 2.
        """
        logging.debug(f"creating controller {name} with id: {id}")
        self._joystick = pygame.joystick.Joystick(id)
        self._joystick.init()

        self._id = id
        self._ndigit = ndigit

        file_name = f"{name.lower().replace(' ', '_')}.json"
        config_file = os.path.join(self.CONFIG_ROOT_DIR, file_name)
        with open(config_file) as raw_config:
            self._config = json.load(raw_config)

    @classmethod
    def list_connected(cls):
        """
        List the connected and supported controller.

        Return:
            A list containing the controller names. The index of the names correspond
            to the controller ID.
        """
        logging.debug('listing connected/supported controller')
        connected_controllers = []
        for id in range(pygame.joystick.get_count()):
            controller_name = pygame.joystick.Joystick(id).get_name()
            connected_controllers.append(controller_name)

        supported_controllers = [f.replace('.json', '') for f in os.listdir(cls.CONFIG_ROOT_DIR)]
        conn_supp_controllers = filter(
            lambda ctrl : any(ctrl.lower().replace(' ', '_') in ctrl_name for ctrl_name in supported_controllers),
            connected_controllers)
        conn_supp_controllers = tuple(conn_supp_controllers)

        logging.debug(f"found the following controllers: {conn_supp_controllers}")

        return conn_supp_controllers

    def get_name(self):
        """
        Get the joystick name.

        Return:
            The name of the controller.
        """
        return self._joystick.get_name()

    def get_id(self):
        """
        Get the joystick id

        Return:
            The ID of the controller.
        """
        return self._id

    def get_buttons(self):
        """
        Get all the buttons state.

        Return:
            A tuple containing all the buttons state. 1 is pressed, 0 is depressed.
        """
        logging.debug(f"reading all button state of controller {self.get_name()}")
        button_count = self._joystick.get_numbuttons()
        button_states = [int(self._joystick.get_button(i)) for i in range(button_count)]

        logging.debug(f"button states: {button_states}")

        return (button_states)

    def get_funct_mapping(self):
        """
        Get the buttons function mapping.

        Return:
            A dictionnary containing the controller buttons funtion mapping.
        """
        return self._config["mapping"]

    def get_button_indexes(self):
        """
        Get the button indexes for the controller.

        Return:
            A dictionnary containing the controller button indexes mapping.
        """
        return self._config["buttons"]

    def get_axis(self):
        """
        Get all axis position.

        Return:
            A tuple containing all the axis positions. The positions are ranging from -1 to 1.
        """
        logging.debug(f"reading all axis positions of controller {self.get_name()}")
        axis_count = self._joystick.get_numaxes()
        axis_positions = [float(self._joystick.get_axis(i)) for i in range(axis_count)]
        axis_positions = [round(pos, self._ndigit) for pos in axis_positions]

        logging.debug(f"axis positions: {axis_positions}")

        return (axis_positions)

