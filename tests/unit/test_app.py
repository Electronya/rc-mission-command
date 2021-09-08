import json
from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))
mockedPygame = Mock()
sys.modules['pygame'] = mockedPygame

from app import App, NoAvailableCtrlr     # noqa: E402


class TestApp(TestCase):
    """
    The app module test cases.
    """
    @patch('app.tk.Tk.__init__')
    def setUp(self, mockedTkInit):
        """
        Test cases setup.
        """
        self.testCtrlrList = {'test controller 1': 0, 'test controller 2': 1,
                              'test controller 3': 2, 'test controller 4': 3}
        self.testCtrlrs = [Mock(), Mock(), Mock(), Mock()]
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

    @patch('app.tk.Tk.__init__')
    def test_contructorInitLogger(self, mockedTkInit):
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

    @patch('app.tk.Tk.__init__')
    def test_constructorInitPygame(self, mockedTkInit):
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

    @patch('app.tk.Tk.__init__')
    def test_constructorInitMqttClient(self, mockedTkInit):
        """
        The constructor must initialize the MQTT client.
        """
        with patch.object(App, '_initLogger') as mockedInitLog, \
                patch.object(App, '_initPygame'), \
                patch.object(App, '_initMqttClient') as mockedInitClient, \
                patch.object(App, '_initControllers'), \
                patch.object(App, '_initUsrInterface'), \
                patch.object(App, 'after'):
            mockedInitLog.return_value = self.testLogger
            testApp = App()     # noqa: F841
            mockedInitClient.assert_called_once_with(self.testLogger)

    @patch('app.tk.Tk.__init__')
    def test_constructorInitControllers(self, mockedTkInit):
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

    @patch('app.tk.Tk.__init__')
    def test_constructorInitUsrInterface(self, mockedTkInit):
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

    @patch('app.tk.Tk.__init__')
    def test_constructorStartEventLoop(self, mockedTkInit):
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

    def test_initMqttClient(self):
        """
        The _initMqttClient method must initialize the MQTT client.
        """
        with patch('app.client') as mockedClient:
            mockedAppLogger = Mock()
            self.testApp._initMqttClient(mockedAppLogger)
            mockedClient.init.assert_called_once_with(mockedAppLogger,
                                                      App.CLIENT_ID,
                                                      App.CLIENT_PASSWD)

    def test_listControllersNoAvailable(self):
        """
        The _listControllers method must raise a NoAvailableCtrlr exception
        if no controller have been found.
        """
        with patch('app.Controller.listControllers') as mockedListCtrlrs, \
                self.assertRaises(NoAvailableCtrlr) as context:
            mockedListCtrlrs.return_value = ()
            self.testApp._listControllers()
            self.assertTrue(isinstance(context.exception, NoAvailableCtrlr))

    def test_listControllers(self):
        """
        The _listControllers method must return the list of all
        available controllers.
        """
        with patch('app.Controller.listControllers') as mockedListCtrlrs:
            mockedListCtrlrs.return_value = self.testCtrlrList
            testResult = self.testApp._listControllers()
            self.assertEqual(testResult, self.testCtrlrList)

    def test_initControllersList(self):
        """
        The _initControllers method must list the available controllers.
        """
        with patch.object(self.testApp, '_listControllers') \
                as mockedListCtrlrs, \
                patch('app.Controller') as mockedCtrlr:
            mockedListCtrlrs.return_value = self.testCtrlrList
            mockedCtrlr.side_effect = self.testCtrlrs
            self.testApp._initControllers(self.testLogger)
            mockedListCtrlrs.assert_called_once()

    def test_initControllersNewInstances(self):
        """
        The _initcontrollers method must create an new Controller isntance
        for each available controller.
        """
        expectedCalls = []
        for ctrlrName in self.testCtrlrList.keys():
            expectedCalls.append(call(self.testLogger,
                                      self.testCtrlrList[ctrlrName],
                                      ctrlrName))
        with patch.object(self.testApp, '_listControllers') \
                as mockedListCtrlrs, \
                patch('app.Controller') as mockedCtrlr:
            mockedListCtrlrs.return_value = self.testCtrlrList
            mockedCtrlr.side_effect = self.testCtrlrs
            self.testApp._initControllers(self.testLogger)
            mockedCtrlr.assert_has_calls(expectedCalls)

    def test_initControllersActivateFirst(self):
        """
        The _initControllers method must activate the first
        controller in the list.
        """
        with patch.object(self.testApp, '_listControllers') \
                as mockedListCtrlrs, \
                patch('app.Controller') as mockedCtrlr:
            mockedListCtrlrs.return_value = self.testCtrlrList
            mockedCtrlr.side_effect = self.testCtrlrs
            self.testApp._initControllers(self.testLogger)
            self.assertEqual(self.testApp._controllers['active'],
                             self.testCtrlrs[0])
