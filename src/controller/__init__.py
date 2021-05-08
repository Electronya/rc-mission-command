import json
import logging
import os

import inputs

class Controller:
    """
    Class implementing the controller function.
    """
    CONFIG_ROOT_DIR = './src/controller/configs/'

    def __init__(self, idx, name, client):
        """
        Constructor.

        Params:
            idx:    The index of the controller in the list of connected gamepads.
            name:   The controller name.
            client: The MQTT client.
        """
        logging.debug(f"creating controller {name} with at index {idx}.")
        self._gamepad = inputs.devices.gamepads[idx]

        self._idx = idx
        self._client = client

        file_name = f"{name.lower().replace(' ', '_')}.json"
        config_file = os.path.join(self.CONFIG_ROOT_DIR, file_name)
        with open(config_file) as raw_config:
            self._config = json.load(raw_config)

    @classmethod
    def list_connected(cls):
        """
        List the connected controllers.

        Return:
            A Dictionary containing the identification of the controller (index: name).
        """
        connected = []
        for gamepad in inputs.devices.gamepads:
            name = gamepad.__str__()
            cut_idx = name.index(' ')
            name = name[cut_idx+1:]
            connected.append(name)

        logging.debug(f"connected controller: {connected}")

        supported = [f.replace('.json', '') for f in os.listdir(cls.CONFIG_ROOT_DIR)]
        logging.debug(f"supported controller: {supported}")

        connected_supported = {}
        for idx in range(len(connected)):
            for supp in supported:
                if supp == connected[idx].lower().replace(' ', '_'):
                    connected_supported[idx] = connected[idx]

        return connected_supported

    def process_events(self):
        """
        Process the controller events.
        """
        for event in self._gamepad.read():
            logging.debug(f"processing event: {event.code}")


    def _funct_mapping(self):
        """
        Get the buttons function mapping.

        Return:
            A dictionnary containing the controller buttons funtion mapping.
        """
        return self._config["mapping"]

    def _button_events(self):
        """
        Get the button events for the controller.

        Return:
            A dictionnary containing the controller button events mapping.
        """
        return self._config["buttons"]

    def _axis_events(self):
        """
        Get all axis events for the controller.

        Return:
            A dictionnary containing the controller axis events mapping.
        """
        return self._config["axis"]

