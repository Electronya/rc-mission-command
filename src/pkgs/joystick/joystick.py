import json
import os

from PySide2.QtCore import QObject, QThreadPool, QTimer, Signal

import pygame as pg
from pygame import joystick

from .joystickProcessor import JoystickProcessor


class Joystick(QObject):
    """
    Class implementing the joystick function.
    """
    CONFIG_ROOT_DIR = './src/pkgs/joystick/configs/'
    TYPE_KEY = 'type'
    AXES_KEY = 'axes'
    BTNS_KEY = 'buttons'
    HATS_KEY = 'hats'
    CAL_SEQ = 6
    FRAME_PERIOD_MS = 10

    axisMotion = Signal(str, int, float)
    buttonDown = Signal(str, int)
    buttonUp = Signal(str, int)
    hatMotion = Signal(str, int, tuple)

    def __init__(self, logger: object, idx: int,
                 name: str, ndigit: int = 2) -> None:
        """
        Constructor.

        Params:
            dispatcher:     The application event dispatcher.
            logger:         The application logger.
            idx:            The index of the joystick from 0 to
                            pygame.joystick.get_count().
            name:           The joystick name.
            ndigit:         The digit number for the axis precision.
                            Default: 2.
        """
        QObject.__init__(self)
        self._logger = logger.getLogger(f"JOYSTICK_{idx}")
        self._idx = idx
        self._ndigit = ndigit
        self._isCalibrated = False
        self._logger.info(f"creating joystick {name}")
        self._joystick = joystick.Joystick(idx)
        self._joystick.init()
        filename = f"{name.lower().replace(' ', '_')}.json"
        configFilePath = os.path.join(self.CONFIG_ROOT_DIR, filename)
        with open(configFilePath) as configFile:
            self._config = json.load(configFile)

        self._axes = [{"min": 0.0, "max": 0.0}] * \
            len(self._config[self.AXES_KEY])
        self._buttons = [False] * \
            len(self._config[self.BTNS_KEY])
        self._hats = [{"min": 0.0, "max": 0.0}] * \
            len(self._config[self.HATS_KEY])

        self._setupProcessor()

    @classmethod
    def initFramework(cls):
        """
        Initialize the pygame framework.
        """
        pg.init()
        pg.event.set_allowed([pg.JOYAXISMOTION, pg.JOYBUTTONDOWN,
                              pg.JOYBUTTONUP, pg.JOYHATMOTION])

    @classmethod
    def _listConnected(cls) -> tuple:
        """
        List the connected joystick.

        Params:
            logger:     The logger.

        Returns:
            The list of connected joystick.
        """
        connected = []
        for ctrlrId in range(joystick.get_count()):
            ctrlrName = joystick.Joystick(ctrlrId).get_name()
            connected.append(ctrlrName)
        return tuple(connected)

    @classmethod
    def _filterUnsupported(cls, connected: tuple, supported: tuple) -> dict:
        """
        Filter the unsupported joystick.

        Params:
            connected:  The list of connected joystick.
            supported:  The list of supported joystick.

        Return:
            A dictionary listing the filtered joysticks
        """
        filteredCtrlrs = {}
        for idx, ctrlrName in enumerate(connected):
            if any(ctrlrName.lower().replace(' ', '_')
                   in suppCtrlr for suppCtrlr in supported):
                filteredCtrlrs[connected[idx]] = idx
        return filteredCtrlrs

    @classmethod
    def listAvailable(cls) -> dict:
        """
        List the available joystick.

        Return:
            A Dictionary listing the available joystick.
            The keys is the joystick name and the value is its index.
        """
        connected = cls._listConnected()
        supported = (f.replace('.json', '')
                     for f in os.listdir(cls.CONFIG_ROOT_DIR))
        connected_supported = cls._filterUnsupported(connected,
                                                     tuple(supported))
        return connected_supported

    def _calculateModifier(self, limits, val) -> float:
        """
        Calculate modifier.

        Params:
            limits:     The axis/hat limit values.
            val:        The axis/hat actual value.

        Return:
            The axis/hat modifier.
        """
        modifier = 0.0
        if limits['min'] < 0 and val < 0:
            modifier = round(abs(val) / limits['min'], self._ndigit)
        elif limits['min'] < 0 and val > 0:
            modifier = round(val / limits['max'], self._ndigit)
        else:
            modifier = round(abs(limits['min'] - val) /
                             (limits['max'] - limits['min']),
                             self._ndigit)
        return modifier

    def _processAxisSignal(self, idx, position) -> None:
        """
        Process axis signals.

        Params:
            idx:        The axis index.
            position:   The axis position.
        """
        self._logger.debug(f"processing axis {idx} signal with "
                           f"position: {position}")
        modifier = self._calculateModifier(self._axes[idx], position)
        self._logger.info(f"new axis{idx} modifier: {modifier}")
        self.axisMotion.emit(self._config[self.TYPE_KEY], idx, modifier)

    def _processBtnDownSignal(self, idx):
        """
        Process button down signals.

        Params:
            idx:        The button index.
        """
        self._logger.info(f"button {idx} is pressed")
        self.buttonDown.emit(self._config[self.TYPE_KEY], idx)

    def _processBtnUpSignal(self, idx):
        """
        Process button up signals.

        Params:
            idx:        The button index.
        """
        self._logger.info(f"button {idx} is depressed")
        self.buttonUp.emit(self._config[self.TYPE_KEY], idx)

    def _processHatSignal(self, idx, vals) -> None:
        """
        Process hat signals.

        Params:
            idx:        The hat index.
            vals:       The hat x and y values.
        """
        self._logger.debug(f"processing hat {idx} signal with "
                           f"position: {vals}")
        self.hatMotion.emit(self._config[self.TYPE_KEY], idx, vals)

    def _startProcessing(self):
        """
        Start the processing worker.
        """
        worker = JoystickProcessor(self._logger)
        worker.signals.axisMotion \
            .connect(lambda idx, val: self._processAxisSignal(idx, val))
        worker.signals.hatMotion \
            .connect(lambda idx, val: self._processHatSignal(idx, val))
        worker.signals.buttonDown \
            .connect(lambda idx: self._processBtnDownSignal(idx))
        worker.signals.buttonUp \
            .connect(lambda idx: self._processBtnUpSignal(idx))
        self._threadPool.start(worker)

    def _setupProcessor(self):
        """
        Setup the joystick event processor.
        """
        self._threadPool = QThreadPool.globalInstance()
        self._processTimer = QTimer(self)
        self._processTimer.timeout.connect(self._startProcessing)

    def getName(self) -> str:
        """
        Get the joystick name.

        Return:
            The name of the joystick.
        """
        return self._joystick.get_name()

    def getIdx(self) -> int:
        """
        Get the joystick index

        Return:
            The index of the joystick.
        """
        return self._idx

    def getType(self) -> str:
        """
        Get the joystick type.

        Return:
            The joystick type.
        """
        return self._config[self.TYPE_KEY]

    def activate(self):
        """
        Activate the joystick.
        """
        self._logger.info('activating')
        self._processTimer.start(self.FRAME_PERIOD_MS)

    def deactivate(self):
        """
        Deactivate the joystick.
        """
        self._logger.info('deactivating')
        self._processTimer.stop()

    def quit(self) -> None:
        """
        Uninitialized the joystick.
        """
        self._logger.info('unitializing joystick')
        self._joystick.quit()