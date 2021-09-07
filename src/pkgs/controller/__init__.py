import json
import os

from pygame import joystick


class Controller:
    """
    Class implementing the controller function.
    """
    CONFIG_ROOT_DIR = './src/pkgs/controller/configs/'
    CTRL_FRAME_RATE = 10

    def __init__(self, logger: object, idx: int,
                 name: str, ndigit: int = 2) -> None:
        """
        Constructor.

        Params:
            logger:     The application logger.
            idx:        The index of the controller from 0 to
                        pygame.joystick.get_count().
            name:       The controller name.
            ndigit:     The digit number for the axis precision. Default: 2.
        """
        self._logger = logger.getLogger(f"CTRL_{idx}")
        self._idx = idx
        self._ndigit = ndigit
        self._isCalibrated = False
        self._calibrationSeq = 0
        self._logger.info(f"creating controller {name}")
        self._joystick = joystick.Joystick(idx)
        self._joystick.init()
        filename = f"{name.lower().replace(' ', '_')}.json"
        configFilePath = os.path.join(self.CONFIG_ROOT_DIR, filename)
        with open(configFilePath) as configFile:
            self._config = json.load(configFile)
        self._calibrationSeq = [
            self._saveSteeringLeft,
            self._saveSteeringRight,
            self._saveThrottleOff,
            self._saveThrottleFull,
            self._saveBrakeOff,
            self._saveBrakeFull
        ]
        self._axisGetters = [
            self._getSteeringModifier,
            self._getThrottleModifier,
            self._getBrakeModifier
        ]

    @classmethod
    def _listConnected(cls) -> tuple:
        """
        List the connected controller.

        Params:
            logger:     The logger.

        Returns:
            The list of connected controller.
        """
        connected = []
        for ctrlrId in range(joystick.get_count()):
            ctrlrName = joystick.Joystick(ctrlrId).get_name()
            connected.append(ctrlrName)
        return tuple(connected)

    @classmethod
    def _filterUnsupported(cls, connected: tuple, supported: tuple) -> dict:
        """
        Filter the unsupported controller.

        Params:
            connected:  The list of connected controller.
            supported:  The list of supported controller.
        """
        connected_supported = {}
        for idx in range(len(connected)):
            if any(connected[idx].lower().replace(' ', '_')
                   in ctrl_name for ctrl_name in supported):
                connected_supported[connected[idx]] = idx
        return connected_supported

    @classmethod
    def listController(cls) -> dict:
        """
        List the connected and supported controller.

        Return:
            A Dictionary listing the connected and supported controller.
            The keys is the controller name and the value is its index.
        """
        connected = cls._listConnected()
        supported = (f.replace('.json', '')
                     for f in os.listdir(cls.CONFIG_ROOT_DIR))
        connected_supported = cls._filterUnsupported(connected,
                                                     tuple(supported))
        return connected_supported

    def _saveSteeringLeft(self) -> None:
        """
        Save the left position of the steering.
        """
        fullLeftSteering = \
            self._joystick.get_axis(self.get_axis_map().index('steering'))
        self._steeringLeft = abs(fullLeftSteering)
        self._logger.debug(f"saving steering left position as "
                           f"{self._steeringLeft}")

    def _saveSteeringRight(self):
        """
        Save the right position of the steering.
        """
        fullRightSteering = \
            self._joystick.get_axis(self.get_axis_map().index('steering'))
        self._steeringRight = abs(fullRightSteering)
        self._logger.debug(f"saving steering left position as "
                           f"{self._steeringRight}")

    def _saveThrottleOff(self):
        """
        Save the throttle off position.
        """
        throttleOff = \
            self._joystick.get_axis(self.get_axis_map().index('throttle'))
        self._throttleOff = abs(throttleOff)
        self._logger.debug(f"saving throttle off position as "
                           f"{self._throttleOff}")

    def _saveThrottleFull(self):
        """
        Save the throttle full position.
        """
        throttleFull = \
            self._joystick.get_axis(self.get_axis_map().index('throttle'))
        self._throttleFull = abs(throttleFull)
        self._logger.debug(f"saving throttle full position as "
                           f"{self._throttleFull}")

    def _saveBrakeOff(self):
        """
        Save the break off position.
        """
        brakeOff = \
            self._joystick.get_axis(self.get_axis_map().index('brake'))
        self._brakeOff = abs(brakeOff)
        self._logger.debug(f"saving break off position as {self._brakeOff}")

    def _saveBrakeFull(self):
        """
        Save the break full position.
        """
        brakeFull = \
            self._joystick.get_axis(self.get_axis_map().index('brake'))
        self._brakeFull = abs(brakeFull)
        self._logger.debug(f"saving break full position as {self._brakeFull}")

    def _getSteeringModifier(self):
        """
        Get the steering modifier.

        Return:
            The steering modifier.
        """
        steeringPos = self._joystick.get_axis(self._config['controls']['axis'].index('steering'))
        modifier = 0
        if steeringPos < 0:
            modifier = round(steeringPos / self._steeringLeft, 2)
        else:
            modifier = round(steeringPos / self._steeringRight, 2)

        self._logger.debug(f"steering modifier: {modifier}")
        return modifier

    def _getThrottleModifier(self):
        """
        Get the throttle modifier.

        Return:
            The throttle modifier.
        """
        throttlePos = self._joystick.get_axis(self._config['controls']['axis'].index('throttle'))
        modifier = round((self._throttleFull - throttlePos) / (self._throttleFull - self._throttleOff), 2)
        modifier = 1 - modifier
        self._logger.debug(f"throttle modifier: {modifier}")
        return modifier

    def _getBrakeModifier(self):
        """
        Get the break modifier.

        Return:
            The break modifier.
        """
        breakPos = self._joystick.get_axis(self._config['controls']['axis'].index('brake'))
        modifier = round((self._brakeFull - breakPos) / (self._brakeFull - self._brakeOff), 2)
        modifier = 1 - modifier
        self._logger.debug(f"break modifier: {modifier}")
        return modifier

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

    def is_calibrated(self):
        """
        Get the controller calibartion state.

        Return:
            True if the controller is calibrated, False otherwise.
        """
        return self._isCalibrated

    def get_axis(self, axis):
        """
        Get the current axis position.

        Params:
            axis:       The axis index.
        """
        return self._axisGetters[axis]()

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

    def calibrate(self, seq):
        """
        Calibrate the controller.

        Params:
            seq:        The calibration sequence.
        """
        self._logger.info(f"calibration seq: {seq}.")
        self._calibrationSeq[seq]()
        if seq == (len(self._calibrationSeq) - 1):
            self._isCalibrated = True

    def quit(self):
        """
        Uninitialize the controller.
        """
        self._logger.info(f"unitializing controller")
        self._joystick.quit()
