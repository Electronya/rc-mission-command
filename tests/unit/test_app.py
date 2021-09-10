import json
import tkinter as tk
from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))
mockedPygame = Mock()
sys.modules['pygame'] = mockedPygame

from app import App, NoAvailableCtrlr   # noqa: E402


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
            self.testApp._controllers = {'active': self.testCtrlrs[0],
                                         'list': self.testCtrlrs}
            mockedPygame.JOYAXISMOTION = 0
            mockedPygame.JOYBUTTONDOWN = 1
            mockedPygame.JOYBUTTONUP = 2
            mockedPygame.JOYHATMOTION = 3

    def tearDown(self):
        """
        Test cases tear down.
        """
        mockedPygame.reset_mock()

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
                                                testApp._processCtrlrEvents)

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

    def test_setUsrInterfaceStyle(self):
        """
        The _initUsrInterface method must set th UI style.
        """
        mockedStyle = Mock()
        expectedConfCalls = [call("red.Horizontal.TProgressbar",
                                  foreground='red', background='red'),
                             call("grn.Horizontal.TProgressbar",
                                  foreground='green', background='green')]
        with patch('app.ttk.Style') as mockedTkStyle:
            mockedTkStyle.return_value = mockedStyle
            self.testApp._setUsrInterfaceStyle()
            mockedStyle.theme_use.assert_called_once_with('clam')
            mockedStyle.configure.assert_has_calls(expectedConfCalls)

    def test_initUsrInterfaceTitleAttr(self):
        """
        The _initUsrInterface method must set the application windows title
        and attributes.
        """
        with patch.object(self.testApp, 'title') as mockedTitle, \
                patch.object(self.testApp, 'attributes') as mockedAttributes, \
                patch.object(self.testApp, '_setUsrInterfaceStyle'), \
                patch('app.BaseFrame'):
            self.testApp._initUsrInterface()
            mockedTitle.assert_called_once_with(App.WINDOW_TITLE)
            mockedAttributes.assert_called_once_with('-zoomed', True)

    def test_initUsrInterfaceStyle(self):
        """
        The _initUsrInterface method must set the application style.
        """
        with patch.object(self.testApp, 'title'), \
                patch.object(self.testApp, 'attributes'), \
                patch.object(self.testApp, '_setUsrInterfaceStyle') \
                as mockedSetUsrIfaceStyle, \
                patch('app.BaseFrame'):
            self.testApp._initUsrInterface()
            mockedSetUsrIfaceStyle.assert_called_once()

    def test_initUsrInterfaceBaseFame(self):
        """
        The _initUsrInterface method must initialize and display the base fame.
        """
        mockedBaseFrame = Mock()
        with patch.object(self.testApp, 'title'), \
                patch.object(self.testApp, 'attributes'), \
                patch.object(self.testApp, '_setUsrInterfaceStyle'), \
                patch('app.BaseFrame') as mockedBaseFrmcls:
            mockedBaseFrmcls.return_value = mockedBaseFrame
            self.testApp._initUsrInterface()
            mockedBaseFrmcls.assert_called_once_with(self.testApp,
                                                     self.testApp._controllers,   # noqa: E501
                                                     self.testApp._units)
            mockedBaseFrame.pack.assert_called_once_with(fill=tk.BOTH,
                                                         expand=True)

    def test_processCtrlrEvents(self):
        """
        The _processCtrlrEvents must process the event of the
        active controller.
        """
        with patch.object(self.testApp, 'after'):
            self.testApp._processCtrlrEvents()
            self.testApp._controllers['active'].processEvents.assert_called_once()  # noqa: E501

    def test_processCtrlrEventsLoop(self):
        """
        The _processCtrlrEvents must keep the loop going.
        """
        with patch.object(self.testApp, 'after') as mockedAfter:
            mockedPygame.event.get.return_value = []
            self.testApp._processCtrlrEvents()
            mockedAfter.assert_called_once_with(self.testApp.CTRL_FRAME_RATE,
                                                self.testApp._processCtrlrEvents)  # noqa: E501

    def test_quitCtrlrs(self):
        """
        The quit method must quit all controllers.
        """
        with patch('app.client'), \
                patch.object(self.testApp, 'destroy'), \
                patch('app.sys'):
            self.testApp.quit()
            for ctrlrs in self.testApp._controllers['list']:
                ctrlrs.quit.assert_called_once()

    def test_quitPygame(self):
        """
        The quit method must quit pygame
        """
        with patch('app.client'), \
                patch.object(self.testApp, 'destroy'), \
                patch('app.sys'):
            self.testApp.quit()
            mockedPygame.quit.assert_called_once()

    def test_quitDisconnectClient(self):
        """
        The quit method must disconnect the MQTT client.
        """
        with patch('app.client') as mockedClient, \
                patch.object(self.testApp, 'destroy'), \
                patch('app.sys'):
            self.testApp.quit()
            mockedClient.disconnect.assert_called_once()

    def test_quitDestroyUI(self):
        """
        The quit methos must destroy the application UI.
        """
        with patch('app.client'), \
                patch.object(self.testApp, 'destroy') as mockedDestroy, \
                patch('app.sys'):
            self.testApp.quit()
            mockedDestroy.assert_called_once()

    def test_quitSysExit(self):
        """
        The quit method must exit from the application.
        """
        with patch('app.client'), \
                patch.object(self.testApp, 'destroy'), \
                patch('app.sys') as mockedSys:
            self.testApp.quit()
            mockedSys.exit.asset_called_once_with(0)
