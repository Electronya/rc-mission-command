from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

import pygame as pg

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.joystick import JoystickProcessor     # noqa: E402


class TestJoystickProcessor(TestCase):
    """
    The JoystickProcessor class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.joystickProcessSignalsCls = 'pkgs.joystick.joystickProcessor.JoystickProcessSignals'    # noqa: E501
        self.pgEvent = 'pkgs.joystick.joystickProcessor.pgEvent'
        self.logger = Mock()
        self.mockedSignals = Mock()
        with patch(self.joystickProcessSignalsCls) as mockedJoystickSignalsCls:
            mockedJoystickSignalsCls.return_value = self.mockedSignals
            self.joystickProcessor = JoystickProcessor(self.logger)

    def test_constructorCreateSignals(self):
        """
        The constructor must create the processing signals.
        """
        with patch(self.joystickProcessSignalsCls) as mockedJoystickSignalsCls:
            JoystickProcessor(self.logger)
            mockedJoystickSignalsCls.assert_called_once()

    def test_runEmitAxisMotion(self):
        """
        The run method must emit the axis motion signal
        when the axis motion event happened.
        """
        mockedEvent = MagicMock()
        mockedEvent.type = pg.JOYAXISMOTION
        mockedEvent.instance_id = 0
        mockedEvent.axis = 0
        mockedEvent.value = 0.1
        with patch(f"{self.pgEvent}.get") as mockedPgEventGet:
            mockedPgEventGet.return_value = [mockedEvent]
            self.joystickProcessor.run()
            self.joystickProcessor.signals.axisMotion.emit. \
                assert_called_once_with(mockedEvent.axis,
                                        mockedEvent.value)

    def test_runEmitButtonDown(self):
        """
        The run method must emit the button down signal
        when the button down event happened.
        """
        mockedEvent = MagicMock()
        mockedEvent.type = pg.JOYBUTTONDOWN
        mockedEvent.instance_id = 0
        mockedEvent.button = 1
        with patch(f"{self.pgEvent}.get") as mockedPgEventGet:
            mockedPgEventGet.return_value = [mockedEvent]
            self.joystickProcessor.run()
            self.joystickProcessor.signals.buttonDown.emit. \
                assert_called_once_with(mockedEvent.button)

    def test_runEmitButtonUp(self):
        """
        The run method must emit the button up signal
        when the button up event happened.
        """
        mockedEvent = MagicMock()
        mockedEvent.type = pg.JOYBUTTONUP
        mockedEvent.instance_id = 0
        mockedEvent.button = 2
        with patch(f"{self.pgEvent}.get") as mockedPgEventGet:
            mockedPgEventGet.return_value = [mockedEvent]
            self.joystickProcessor.run()
            self.joystickProcessor.signals.buttonUp.emit. \
                assert_called_once_with(mockedEvent.button)

    def test_runEmitHatMotion(self):
        """
        The run method must emit the hat motion signal
        when the hat motion event happened.
        """
        mockedEvent = MagicMock()
        mockedEvent.type = pg.JOYHATMOTION
        mockedEvent.instance_id = 0
        mockedEvent.hat = 3
        mockedEvent.value = 0.9
        with patch(f"{self.pgEvent}.get") as mockedPgEventGet:
            mockedPgEventGet.return_value = [mockedEvent]
            self.joystickProcessor.run()
            self.joystickProcessor.signals.hatMotion.emit. \
                assert_called_once_with(mockedEvent.hat,
                                        mockedEvent.value)
