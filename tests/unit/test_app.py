import json
import tkinter as tk
from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))
mockedPygame = Mock()
sys.modules['pygame'] = mockedPygame

# from app import App, NoAvailableCtrlr   # noqa: E402
# from pkgs.messages.unitCxnStateMsg import UnitCxnStateMsg   # noqa: E402


class TestApp(TestCase):
    """
    The app module test cases.
    """
    # @patch('app.tk.Tk.__init__')
    # def setUp(self, mockedTkInit):
    #     """
    #     Test cases setup.
    #     """
    #     self.testCtrlrList = {'test controller 1': 0, 'test controller 2': 1,
    #                           'test controller 3': 2, 'test controller 4': 3}
    #     self.testUnitId = 'test unit'
    #     testCxnState = {}
    #     testCxnState[UnitCxnStateMsg.UNIT_ID_KEY] = self.testUnitId
    #     testCxnState[UnitCxnStateMsg.PAYLOAD_KEY] = {}
    #     testCxnState[UnitCxnStateMsg.PAYLOAD_KEY][UnitCxnStateMsg.STATE_KEY] = UnitCxnStateMsg.ONLINE_STATE     # noqa: E501
    #     self.testCxnStateJson = json.dumps(testCxnState)
    #     self.testCtrlrs = [Mock(), Mock(), Mock(), Mock()]
    #     self.testUnits = [Mock(), Mock(), Mock(), Mock()]
    #     self.testLogger = Mock()
    #     with patch.object(App, '_initLogger') as mockedInitLog, \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after'):
    #         mockedInitLog.return_value = self.testLogger
    #         self.testApp = App()
    #         self.testApp._logger = Mock()
    #         self.testApp._controllers = {'active': self.testCtrlrs[0],
    #                                      'list': self.testCtrlrs}
    #         units = self.testUnits.copy()
    #         self.testApp._units = {'active': units[0],
    #                                'list': units}
    #         mockedPygame.JOYAXISMOTION = 0
    #         mockedPygame.JOYBUTTONDOWN = 1
    #         mockedPygame.JOYBUTTONUP = 2
    #         mockedPygame.JOYHATMOTION = 3

    # def tearDown(self):
    #     """
    #     Test cases tear down.
    #     """
    #     mockedPygame.reset_mock()

    # @patch('app.tk.Tk.__init__')
    # def test_constructorInitTk(self, mockedTkInit):
    #     """
    #     The constructor must initialize the Tk class.
    #     """
    #     with patch.object(App, '_initLogger'), \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after'):
    #         testApp = App()
    #         mockedTkInit.assert_called_once_with(testApp)

    # @patch('app.tk.Tk.__init__')
    # def test_contructorInitLogger(self, mockedTkInit):
    #     """
    #     The constructor must initialize the application logger.
    #     """
    #     with patch.object(App, '_initLogger') as mockedInitLog, \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after'):
    #         testApp = App()     # noqa: F841
    #         mockedInitLog.assert_called_once()

    # @patch('app.tk.Tk.__init__')
    # def test_constructorInitPygame(self, mockedTkInit):
    #     """
    #     The constructor must initialize the pygame pakage.
    #     """
    #     with patch.object(App, '_initLogger'), \
    #             patch.object(App, '_initPygame') as mockedInitPygame, \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after'):
    #         testApp = App()     # noqa: F841
    #         mockedInitPygame.assert_called_once()

    # @patch('app.tk.Tk.__init__')
    # def test_constructorInitMqttClient(self, mockedTkInit):
    #     """
    #     The constructor must initialize the MQTT client.
    #     """
    #     with patch.object(App, '_initLogger') as mockedInitLog, \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient') as mockedInitClient, \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after'):
    #         mockedInitLog.return_value = self.testLogger
    #         testApp = App()     # noqa: F841
    #         mockedInitClient.assert_called_once_with(self.testLogger)

    # @patch('app.tk.Tk.__init__')
    # def test_constructorInitControllers(self, mockedTkInit):
    #     """
    #     The constructor must initialize the controllers.
    #     """
    #     with patch.object(App, '_initLogger') as mockedInitLog, \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers') as mockedInitCtrls, \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after'):
    #         mockedInitLog.return_value = self.testLogger
    #         testApp = App()     # noqa: F841
    #         mockedInitCtrls.assert_called_once_with(self.testLogger)

    # @patch('app.tk.Tk.__init__')
    # def test_constructorInitUsrInterface(self, mockedTkInit):
    #     """
    #     The constructor must initialize the user interface.
    #     """
    #     with patch.object(App, '_initLogger'), \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface') as mockedInitUI, \
    #             patch.object(App, 'after'):
    #         testApp = App()     # noqa: F841
    #         mockedInitUI.assert_called_once()

    # @patch('app.tk.Tk.__init__')
    # def test_constructorStartEventLoop(self, mockedTkInit):
    #     """
    #     The constructor must start the event loop.
    #     """
    #     with patch.object(App, '_initLogger'), \
    #             patch.object(App, '_initPygame'), \
    #             patch.object(App, '_initMqttClient'), \
    #             patch.object(App, '_initControllers'), \
    #             patch.object(App, '_initUsrInterface'), \
    #             patch.object(App, 'after') as mockedAfter:
    #         testApp = App()
    #         mockedAfter.assert_called_once_with(testApp.CTRL_FRAME_RATE,
    #                                             testApp._processCtrlrEvents)

    # def test_initLogger(self):
    #     """
    #     The _initLogger method must initialize the application logger,
    #     create the class logger and return the application logger.
    #     """
    #     with patch('app.initLogger') as mockedInitLogger:
    #         mockedInitLogger.return_value = self.testLogger
    #         testResult = self.testApp._initLogger()
    #         mockedInitLogger.assert_called_once()
    #         self.testLogger.getLogger.assert_called_once_with('APP')
    #         self.assertEqual(testResult, self.testLogger)

    # def test_initPygame(self):
    #     """
    #     The _initPygame method must initialize the pygame pakage
    #     and set the allowed event.
    #     """
    #     expectedEvents = [mockedPygame.JOYAXISMOTION,
    #                       mockedPygame.JOYBUTTONDOWN,
    #                       mockedPygame.JOYBUTTONUP,
    #                       mockedPygame.JOYHATMOTION]
    #     self.testApp._initPygame()
    #     mockedPygame.init.assert_called_once()
    #     mockedPygame.event.set_allowed.assert_called_once_with(expectedEvents)

    # def test_initMqttClient(self):
    #     """
    #     The _initMqttClient method must initialize the MQTT client.
    #     """
    #     with patch('app.client') as mockedClient:
    #         mockedAppLogger = Mock()
    #         self.testApp._initMqttClient(mockedAppLogger)
    #         mockedClient.init.assert_called_once_with(mockedAppLogger,
    #                                                   App.CLIENT_ID,
    #                                                   App.CLIENT_PASSWD)

    # def test_initMqttClientCxnStateCallback(self):
    #     """
    #     The _initMqttClient method must register the connection sate
    #     message callback.
    #     """
    #     with patch('app.client') as mockedClient:
    #         mockedAppLogger = Mock()
    #         self.testApp._initMqttClient(mockedAppLogger)
    #         mockedClient.registerMsgCallback.assert_called_once_with(UnitCxnStateMsg.TOPIC_ROOT,    # noqa: E501
    #                                                                  self.testApp._onCxnStateMsg)   # noqa: E501

    # def test_initMqttClientStartLoop(self):
    #     """
    #     The _initMqttClient method must start the client network loop.
    #     """
    #     with patch('app.client') as mockedClient:
    #         mockedAppLogger = Mock()
    #         self.testApp._initMqttClient(mockedAppLogger)
    #         mockedClient.startLoop.assert_called_once()

    # def test_listControllersNoAvailable(self):
    #     """
    #     The _listControllers method must raise a NoAvailableCtrlr exception
    #     if no controller have been found.
    #     """
    #     with patch('app.Controller.listControllers') as mockedListCtrlrs, \
    #             self.assertRaises(NoAvailableCtrlr) as context:
    #         mockedListCtrlrs.return_value = ()
    #         self.testApp._listControllers()
    #         self.assertTrue(isinstance(context.exception, NoAvailableCtrlr))

    # def test_listControllers(self):
    #     """
    #     The _listControllers method must return the list of all
    #     available controllers.
    #     """
    #     with patch('app.Controller.listControllers') as mockedListCtrlrs:
    #         mockedListCtrlrs.return_value = self.testCtrlrList
    #         testResult = self.testApp._listControllers()
    #         self.assertEqual(testResult, self.testCtrlrList)

    # def test_initControllersList(self):
    #     """
    #     The _initControllers method must list the available controllers.
    #     """
    #     with patch.object(self.testApp, '_listControllers') \
    #             as mockedListCtrlrs, \
    #             patch('app.Controller') as mockedCtrlr:
    #         mockedListCtrlrs.return_value = self.testCtrlrList
    #         mockedCtrlr.side_effect = self.testCtrlrs
    #         self.testApp._initControllers(self.testLogger)
    #         mockedListCtrlrs.assert_called_once()

    # def test_initControllersNewInstances(self):
    #     """
    #     The _initcontrollers method must create an new Controller isntance
    #     for each available controller.
    #     """
    #     expectedCalls = []
    #     for ctrlrName in self.testCtrlrList.keys():
    #         expectedCalls.append(call(self.testLogger,
    #                                   self.testCtrlrList[ctrlrName],
    #                                   ctrlrName))
    #     with patch.object(self.testApp, '_listControllers') \
    #             as mockedListCtrlrs, \
    #             patch('app.Controller') as mockedCtrlr:
    #         mockedListCtrlrs.return_value = self.testCtrlrList
    #         mockedCtrlr.side_effect = self.testCtrlrs
    #         self.testApp._initControllers(self.testLogger)
    #         mockedCtrlr.assert_has_calls(expectedCalls)

    # def test_initControllersActivateFirst(self):
    #     """
    #     The _initControllers method must activate the first
    #     controller in the list.
    #     """
    #     with patch.object(self.testApp, '_listControllers') \
    #             as mockedListCtrlrs, \
    #             patch('app.Controller') as mockedCtrlr:
    #         mockedListCtrlrs.return_value = self.testCtrlrList
    #         mockedCtrlr.side_effect = self.testCtrlrs
    #         self.testApp._initControllers(self.testLogger)
    #         self.assertEqual(self.testApp._controllers['active'],
    #                          self.testCtrlrs[0])

    # def test_setUsrInterfaceStyle(self):
    #     """
    #     The _initUsrInterface method must set th UI style.
    #     """
    #     mockedStyle = Mock()
    #     expectedConfCalls = [call("red.Horizontal.TProgressbar",
    #                               foreground='red', background='red'),
    #                          call("grn.Horizontal.TProgressbar",
    #                               foreground='green', background='green')]
    #     with patch('app.ttk.Style') as mockedTkStyle:
    #         mockedTkStyle.return_value = mockedStyle
    #         self.testApp._setUsrInterfaceStyle()
    #         mockedStyle.theme_use.assert_called_once_with('clam')
    #         mockedStyle.configure.assert_has_calls(expectedConfCalls)

    # def test_initUsrInterfaceTitleAttr(self):
    #     """
    #     The _initUsrInterface method must set the application windows title
    #     and attributes.
    #     """
    #     with patch.object(self.testApp, 'title') as mockedTitle, \
    #             patch.object(self.testApp, 'attributes') as mockedAttributes, \
    #             patch.object(self.testApp, '_setUsrInterfaceStyle'), \
    #             patch('app.BaseFrame'):
    #         self.testApp._initUsrInterface()
    #         mockedTitle.assert_called_once_with(App.WINDOW_TITLE)
    #         mockedAttributes.assert_called_once_with('-zoomed', True)

    # def test_initUsrInterfaceStyle(self):
    #     """
    #     The _initUsrInterface method must set the application style.
    #     """
    #     with patch.object(self.testApp, 'title'), \
    #             patch.object(self.testApp, 'attributes'), \
    #             patch.object(self.testApp, '_setUsrInterfaceStyle') \
    #             as mockedSetUsrIfaceStyle, \
    #             patch('app.BaseFrame'):
    #         self.testApp._initUsrInterface()
    #         mockedSetUsrIfaceStyle.assert_called_once()

    # def test_initUsrInterfaceBaseFame(self):
    #     """
    #     The _initUsrInterface method must initialize and display the base fame.
    #     """
    #     mockedBaseFrame = Mock()
    #     with patch.object(self.testApp, 'title'), \
    #             patch.object(self.testApp, 'attributes'), \
    #             patch.object(self.testApp, '_setUsrInterfaceStyle'), \
    #             patch('app.BaseFrame') as mockedBaseFrmcls:
    #         mockedBaseFrmcls.return_value = mockedBaseFrame
    #         self.testApp._initUsrInterface()
    #         mockedBaseFrmcls.assert_called_once_with(self.testApp,
    #                                                  self.testApp._controllers,   # noqa: E501
    #                                                  self.testApp._units)
    #         mockedBaseFrame.pack.assert_called_once_with(fill=tk.BOTH,
    #                                                      expand=True)

    # def test_processCtrlrEvents(self):
    #     """
    #     The _processCtrlrEvents must process the event of the
    #     active controller.
    #     """
    #     with patch.object(self.testApp, 'after'):
    #         self.testApp._processCtrlrEvents()
    #         self.testApp._controllers['active'].processEvents.assert_called_once()  # noqa: E501

    # def test_processCtrlrEventsLoop(self):
    #     """
    #     The _processCtrlrEvents must keep the loop going.
    #     """
    #     with patch.object(self.testApp, 'after') as mockedAfter:
    #         mockedPygame.event.get.return_value = []
    #         self.testApp._processCtrlrEvents()
    #         mockedAfter.assert_called_once_with(self.testApp.CTRL_FRAME_RATE,
    #                                             self.testApp._processCtrlrEvents)  # noqa: E501

    # def test_addUnit(self):
    #     """
    #     The _addUnit method must create the new unit
    #     and add it to the list.
    #     """
    #     newUnit = Mock()
    #     with patch('app.Unit') as mockedUnit, \
    #             patch('app.client') as mockedClient:
    #         mockedUnit.return_value = newUnit
    #         self.testUnits.append(newUnit)
    #         self.testApp._addUnit(self.testUnitId)
    #         mockedUnit.assert_called_once_with(self.testLogger, mockedClient,
    #                                            self.testUnitId)
    #         self.assertEqual(self.testApp._units['list'], self.testUnits)

    # def test_addUnitAlreadyExist(self):
    #     """
    #     The _addUnit method must not add a unit that is already in the list.
    #     """
    #     testUniId = 'test unit'
    #     newUnit = Mock()
    #     self.testApp._units['list'][2].get_id.return_value = testUniId
    #     with patch('app.Unit') as mockedUnit:
    #         mockedUnit.return_value = newUnit
    #         self.testApp._addUnit(testUniId)
    #         mockedUnit.assert_not_called()

    # def test_removeUnit(self):
    #     """
    #     The _removeUnit method must remove the unit with the
    #     provided unit ID from the list set the active on at None
    #     when necessary.
    #     """
    #     self.testApp._units['list'][2].get_id.return_value = self.testUnitId
    #     self.testApp._units['active'] = self.testApp._units['list'][2]
    #     self.testApp._removeUnit(self.testUnitId)
    #     self.assertNotEqual(self.testApp._units['list'],
    #                         self.testUnits)
    #     self.assertEqual(self.testApp._units['active'], None)

    # def test_removeUnitNotFound(self):
    #     """
    #     The _removeUnit method must do nothing if the unit is
    #     not foun in the list.
    #     """
    #     self.testApp._units['active'] = self.testApp._units['list'][2]
    #     self.testApp._removeUnit(self.testUnitId)
    #     self.assertEqual(self.testApp._units['list'],
    #                      self.testUnits)
    #     self.assertEqual(self.testApp._units['active'],
    #                      self.testApp._units['list'][2])

    # def test_onCxnStateMsgCreateMsg(self):
    #     """
    #     The _onCxnStateMsg method must create a UnitCxnStateMsg
    #     from the received JSON message.
    #     """
    #     testCxnMsg = Mock()
    #     with patch('app.UnitCxnStateMsg') as mockedCxnStateMsg, \
    #             patch.object(self.testApp, 'event_generate'):
    #         mockedCxnStateMsg.return_value = testCxnMsg
    #         self.testApp._onCxnStateMsg(None, None, self.testCxnStateJson)
    #         mockedCxnStateMsg.assert_called_once_with(self.testApp.CLIENT_ID)
    #         testCxnMsg.fromJson.assert_called_once_with(self.testCxnStateJson)

    # def test_onCxnStateMsgAddUnit(self):
    #     """
    #     The _onCxnStateMsg method must add a unit if the state received
    #     in online.
    #     """
    #     expectedUnitId = 'test unit'
    #     with patch.object(self.testApp, '_addUnit') as mockedAddUnit, \
    #             patch.object(self.testApp, 'event_generate'):
    #         self.testApp._onCxnStateMsg(None, None, self.testCxnStateJson)
    #         mockedAddUnit.assert_called_once_with(expectedUnitId)

    # def test_onCxnStateMsgRemoveUnit(self):
    #     """
    #     The _onCxnStateMsg method must remove a unit if the state received
    #     in offline.
    #     """
    #     expectedUnitId = 'test unit'
    #     self.testCxnStateJson = \
    #         self.testCxnStateJson.replace(UnitCxnStateMsg.ONLINE_STATE,
    #                                       UnitCxnStateMsg.OFFLINE_STATE)
    #     with patch.object(self.testApp, '_removeUnit') as mockedRemoveUnit, \
    #             patch.object(self.testApp, 'event_generate'):
    #         self.testApp._onCxnStateMsg(None, None, self.testCxnStateJson)
    #         mockedRemoveUnit.assert_called_once_with(expectedUnitId)

    # def test_onCxnStateMsgUpdateEvent(self):
    #     """
    #     The _onCxnStateMsg method must generate an update-unit UI event.
    #     """
    #     expectedUnitId = 'test unit'
    #     testCxnMsg = Mock()
    #     with patch('app.UnitCxnStateMsg') as mockedCxnStateMsg, \
    #             patch.object(self.testApp, 'event_generate') as mockedEventGen:
    #         mockedCxnStateMsg.return_value = testCxnMsg
    #         testCxnMsg.getUnit.return_value = expectedUnitId
    #         self.testApp._onCxnStateMsg(None, None, self.testCxnStateJson)
    #         mockedEventGen.assert_called_once_with('<<update-unit>>')

    # def test_quitCtrlrs(self):
    #     """
    #     The quit method must quit all controllers.
    #     """
    #     with patch('app.client'), \
    #             patch.object(self.testApp, 'destroy'), \
    #             patch('app.sys'):
    #         self.testApp.quit()
    #         for ctrlrs in self.testApp._controllers['list']:
    #             ctrlrs.quit.assert_called_once()

    # def test_quitPygame(self):
    #     """
    #     The quit method must quit pygame
    #     """
    #     with patch('app.client'), \
    #             patch.object(self.testApp, 'destroy'), \
    #             patch('app.sys'):
    #         self.testApp.quit()
    #         mockedPygame.quit.assert_called_once()

    # def test_quitDisconnectClient(self):
    #     """
    #     The quit method must disconnect the MQTT client.
    #     """
    #     with patch('app.client') as mockedClient, \
    #             patch.object(self.testApp, 'destroy'), \
    #             patch('app.sys'):
    #         self.testApp.quit()
    #         mockedClient.disconnect.assert_called_once()

    # def test_quitDestroyUI(self):
    #     """
    #     The quit methos must destroy the application UI.
    #     """
    #     with patch('app.client'), \
    #             patch.object(self.testApp, 'destroy') as mockedDestroy, \
    #             patch('app.sys'):
    #         self.testApp.quit()
    #         mockedDestroy.assert_called_once()

    # def test_quitSysExit(self):
    #     """
    #     The quit method must exit from the application.
    #     """
    #     with patch('app.client'), \
    #             patch.object(self.testApp, 'destroy'), \
    #             patch('app.sys') as mockedSys:
    #         self.testApp.quit()
    #         mockedSys.exit.asset_called_once_with(0)
