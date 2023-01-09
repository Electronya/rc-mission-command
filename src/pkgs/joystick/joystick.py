import json
import logging
import os

from PySide2.QtCore import QObject, QThreadPool, QTimer, Signal, Slot
#test with Q3dAnalogInput

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
    CALIB_KEY = 'calibration'
    FRAME_PERIOD_MS = 10

    axisMotion = Signal(str, int, float)
    buttonDown = Signal(str, int)
    buttonUp = Signal(str, int)
    hatMotion = Signal(str, int, tuple)
    calibration = Signal(str)

    def __init__(self, idx: int, name: str, ndigit: int = 2) -> None:
        """
        Constructor.

        Params:
            idx:            The index of the joystick from 0 to
                            pygame.joystick.get_count().
            name:           The joystick name.
            ndigit:         The digit number for the axis precision.
                            Default: 2.
        """
        QObject.__init__(self)
        self._logger = logging.getLogger(f"joysticks.{idx}")
        self._idx = idx
        self._ndigit = ndigit
        self._isCalibrated = False
        self._calibSeq = 0
        self._logger.info(f"creating joystick {name}")
        self._joystick = joystick.Joystick(idx)
        self._joystick.init()
        filename = f"{name.lower().replace(' ', '_')}.json"
        configFilePath = os.path.join(self.CONFIG_ROOT_DIR, filename)
        with open(configFilePath) as configFile:
            self._config = json.load(configFile)

        self._axes = [{"min": 0.0, "max": 0.0}] * \
            len(self._config[self.AXES_KEY])

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

    def _calculateSplitRangeMod(self, limits: dict, val: float) -> float:
        """
        Calculate split range axis modifier.

        Params:
            limits:     The axis limit values.
            val:        The axis actual value.

        Return:
            The axis modifier.
        """
        modifier = 0.0
        middle = limits['min'] + ((limits['max'] - limits['min']) / 2)
        self._logger.debug(f"calculating modifier with: val={val}, min={limits['min']}, "
                           f"max={limits['max']} and middle={middle}")
        if val < middle:
            self._logger.debug('val < middle')
            modifier = -1 * (abs(val) / abs(middle - limits['min']))
        else:
            self._logger.debug('val > middle')
            modifier = val / (limits['max'] - middle)
        return modifier

    def _calculateFullRangeInvertMod(self, limits: dict, val: float) -> float:
        """
        Calculate full range inverted modifier.

        Params:
            limits:     The axis limit values.
            val:        The axis actual value.

        Return:
            The axis modifier.
        """
        self._logger.debug(f"calculating modifier with: val={val}, "
                           f"min={limits['min']}, max={limits['max']}")
        fullRange = limits['max'] - limits['min']
        modifier = abs(val - limits['min']) / fullRange
        return 1 - modifier

    @Slot(int, float)
    def _processAxisSignal(self, idx: int, position: float) -> None:
        """
        Process axis signals.

        Params:
            idx:        The axis index.
            position:   The axis position.
        """
        calculators = {'steering': self._calculateSplitRangeMod,
                       'throttle': self._calculateFullRangeInvertMod,
                       'brake': self._calculateFullRangeInvertMod}
        print(f"processing axis {idx}")
        if self._isCalibrated:
            modifier = calculators[self._config[self.AXES_KEY][idx]](self._axes[idx], position)     # noqa: E501
            self._logger.debug(f"new axis{idx} modifier: {modifier}")
            self.axisMotion.emit(self._config[self.TYPE_KEY], idx,
                                 round(modifier, self._ndigit))

    @Slot(int)
    def _processBtnDownSignal(self, idx: int) -> None:
        """
        Process button down signals.

        Params:
            idx:        The button index.
        """
        self._logger.info(f"button {idx} is pressed")
        self.buttonDown.emit(self._config[self.TYPE_KEY], idx)

    @Slot(int)
    def _processBtnUpSignal(self, idx: int) -> None:
        """
        Process button up signals.

        Params:
            idx:        The button index.
        """
        self._logger.info(f"button {idx} is depressed")
        self.buttonUp.emit(self._config[self.TYPE_KEY], idx)

    @Slot(int, tuple)
    def _processHatSignal(self, idx: int, vals: int) -> None:
        """
        Process hat signals.

        Params:
            idx:        The hat index.
            vals:       The hat x and y values.
        """
        self._logger.debug(f"processing hat {idx} signal with "
                           f"position: {vals}")
        self.hatMotion.emit(self._config[self.TYPE_KEY], idx, vals)

    def _startProcessing(self) -> None:
        """
        Start the processing worker.
        """
        worker = JoystickProcessor(self._logger)
        worker.signals.axisMotion.connect(self._processAxisSignal)
        worker.signals.hatMotion.connect(self._processHatSignal)
        worker.signals.buttonDown.connect(self._processBtnDownSignal)
        worker.signals.buttonUp.connect(self._processBtnUpSignal)
        self._threadPool.start(worker)

    def _setupProcessor(self) -> None:
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

    def activate(self) -> None:
        """
        Activate the joystick.
        """
        self._logger.info('activating')
        self._processTimer.start(self.FRAME_PERIOD_MS)

    def deactivate(self) -> None:
        """
        Deactivate the joystick.
        """
        self._logger.info('deactivating')
        self._processTimer.stop()

    def calibrate(self) -> None:
        """
        Start the calibration sequence.
        """
        if not self._isCalibrated:
            self._logger.debug(f"joystick {self.getName()} "
                               f"calibartion sequence {self._calibSeq}")
            self._calibSeq += 1
            seq = self._config[self.CALIB_KEY][self._calibSeq - 1]
            if 'axis' in seq:
                axisPos = self._joystick.get_axis(seq['axis'])
                self._logger.debug(f"saving axis {seq['axis']} "
                                   f"{seq['limit']} as {axisPos}")
                self._axes[seq['axis']][seq['limit']] = axisPos
            if self._calibSeq == len(self._config[self.CALIB_KEY]):
                self._calibSeq = 0
                self._isCalibrated = True
            self.calibration.emit(seq['msg'])

    def isCalibrated(self) -> bool:
        """
        Check if the joystick is calibrated.

        Return:
            True if the joystick is calibrated, false otherwise.
        """
        return self._isCalibrated

    def quit(self) -> None:
        """
        Uninitialized the joystick.
        """
        self._logger.info('unitializing joystick')
        self._joystick.quit()
