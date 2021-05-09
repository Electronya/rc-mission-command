import json
import logging
import os

import inputs

class Controller:
    """
    Class implementing the controller function.
    """
    CONFIG_ROOT_DIR = './src/controller/configs/'

    def __init__(self, idx, name, callbacks):
        """
        Constructor.

        Params:
            idx:        The index of the controller in the list of connected gamepads.
            name:       The controller name.
            callacks:   The event callbacks.
        """
        logging.debug(f"creating controller {name} with at index {idx}.")
        self._gamepad = inputs.devices.gamepads[idx]

        self._idx = idx
        self._callbacks = callbacks

        file_name = f"{name.lower().replace(' ', '_')}.json"
        config_file = os.path.join(self.CONFIG_ROOT_DIR, file_name)
        with open(config_file) as raw_config:
            self._config = json.load(raw_config)

        self._isCalibrated = False
        self._updater = {
            'steering': self._update_steering,
        }

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

    def get_name(self):
        """
        Get the controller name.

        Return:
            The controller name.
        """
        name = self._gamepad.__str__()
        cut_idx = name.index(' ')
        return name[cut_idx+1:]

    def is_Calibrate(self):
        """
        Get the calibration state of the controller.

        Return:
            True if the controller is calibrated, false otherwise.
        """
        return self._isCalibrated

    def process_events(self):
        """
        Process the controller events.
        """
        for event in self._gamepad.read():
            if not event.code == 'SYN_REPORT' and not event.code == 'SYN_DROPPED' and not event.code == 'MSC_SCAN':
                logging.debug(f"processing event: {event.code}")
                updater_key = self._config['mapping'][self._config['events'][event.code]]
                logging.debug(f"using updater: {updater_key}")
                # self._updater[updater_key](event.state)

    def _update_steering(self, state):
        """
        Update the steering state.

        Params:
            state:      The steering new state.
        """
        if self._isCalibrated:
            if state > self._steeringCenter:
                modifier = (state - self._steeringCenter) / self._steeringLeftRange
            else:
                modifier = (state - self._steeringCenter) / self._steeringRightRange
            self._callbacks['steering'](modifier)

