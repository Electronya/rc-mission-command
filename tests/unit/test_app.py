import json
from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))
mockedPygame = Mock()
sys.modules['pygame'] = mockedPygame

from app import App     # noqa: E402


class TestApp(TestCase):
    """
    The app module test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.testLogger = Mock()
        with patch.object(App, '_initLogger') as mockedInitLog, \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            mockedInitLog.return_value = self.testLogger
            self.testApp = App()
            self.testApp._logger = Mock()

    @patch('app.tk.Tk.__init__')
    def test_constructorInitTk(self, mockedTkInit):
        """
        The constructor must initialize the Tk class.
        """
        with patch.object(App, '_initLogger'), \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            testApp = App()
            mockedTkInit.assert_called_once_with(testApp)

    def test_contructorInitLogger(self):
        """
        The constructor must initialize the application logger.
        """
        with patch.object(App, '_initLogger') as mockedInitLog, \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            testApp = App()     # noqa: F841
            mockedInitLog.assert_called_once()

    def test_constructorInitPygame(self):
        """
        The constructor must initialize the pygame pakage.
        """
        with patch.object(App, '_initLogger'), \
                patch.object(App, '_initPygame') as mockedInitPygame, \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            testApp = App()     # noqa: F841
            mockedInitPygame.assert_called_once()

    def test_constructorInitMqttClient(self):
        """
        The constructor must initialize the MQTT client.
        """
        with patch.object(App, '_initLogger'), \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient') as mockedInitClient, \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            testApp = App()     # noqa: F841
            mockedInitClient.assert_called_once()

    def test_constructorInitControllers(self):
        """
        The constructor must initialize the controllers.
        """
        with patch.object(App, '_initLogger') as mockedInitLog, \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers') as mockedInitCtrls, \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            mockedInitLog.return_value = self.testLogger
            testApp = App()     # noqa: F841
            mockedInitCtrls.assert_called_once_with(self.testLogger)

    def test_constructorInitUsrInterface(self):
        """
        The constructor must initialize the user interface.
        """
        with patch.object(App, '_initLogger'), \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface') as mockedInitUI, \
                patch.object(App, 'after'):
            testApp = App()     # noqa: F841
            mockedInitUI.assert_called_once()

    def test_constructorStartEventLoop(self):
        """
        The constructor must start the event loop.
        """
        with patch.object(App, '_initLogger'), \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient'), \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after') as mockedAfter:
            testApp = App()
            mockedAfter.assert_called_once_with(testApp.CTRL_FRAME_RATE,
                                                testApp._process_pygame_events)

    def test_initLogger(self):
        """
        The _initLogger method must initialize the application logger,
        create the class logger and return the application logger.
        """
        with patch('app.initLogger') as mockedInitLogger:
            mockedInitLogger.return_value = self.testLogger
            testResult = self.testApp._initLogger()
            mockedInitLogger.assert_called_once()
            self.testLogger.getLogger.assert_called_once_with('APP')
            self.assertEqual(testResult, self.testLogger)

    def test_initPygame(self):
        """
        The _initPygame method must initialize the pygame pakage
        and set the allowed event.
        """
        expectedEvents = [mockedPygame.JOYAXISMOTION,
                          mockedPygame.JOYBUTTONDOWN,
                          mockedPygame.JOYBUTTONUP,
                          mockedPygame.JOYHATMOTION]
        self.testApp._initPygame()
        mockedPygame.init.assert_called_once()
        mockedPygame.event.set_allowed.assert_called_once_with(expectedEvents)
