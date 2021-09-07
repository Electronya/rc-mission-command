from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.controller import Controller  # noqa: E402


class TestController(TestCase):
    """
    The Controller class test cases.
    """
    def setUp(self):
        """
        Teast cases setup.
        """
        self.testLogger = Mock()
        self.testNames = ('test ctrlr 1', 'test ctrlr 2', 'test ctrlr 3')
        self.testIdxes = (0, 1, 2)
        self.testJoysticks = []
        for idx in range(len(self.testNames)):
            mockedJoystick = Mock()
            mockedJoystick.get_name.return_value = self.testNames[idx]
            self.testJoysticks.append(mockedJoystick)
        with open('src/pkgs/controller/configs/logitech_driving_force.json') \
                as configFile:
            self.testConfig = configFile.read()
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch('pkgs.controller.joystick.Joystick') as mockedJoystick:
            mockedJoystick.return_value = self.testJoysticks[0]
            self.testCtrlr = Controller(self.testLogger, 0, self.testNames[0])
        self._setSteeringValues()
        self._setThrottleValues()

    def _setSteeringValues(self):
        """
        Set the test controller steering axis test values.
        """
        self.testCtrlr._steeringLeft = 1
        self.testCtrlr._steeringRight = 1
        self.steeringAxisValues = [-1, -0.5, 0, 0.25, 1]
        self.expectedSteeringMod = []
        for value in self.steeringAxisValues:
            if value < 0:
                modifier = round(value / self.testCtrlr._steeringLeft,
                                 self.testCtrlr._ndigit)
                self.expectedSteeringMod.append(modifier)
            else:
                modifier = round(value / self.testCtrlr._steeringRight,
                                 self.testCtrlr._ndigit)
                self.expectedSteeringMod.append(modifier)

    def _setThrottleValues(self):
        """
        Set the test controller throttle/brake axis test values.
        """
        self.testCtrlr._throttleOff = 1
        self.testCtrlr._throttleFull = 0
        self.testCtrlr._brakeOff = 1
        self.testCtrlr._brakeFull = 0
        self.throttleAxisValues = [0, 0.4, 1, 1, 1]
        self.brakeAxisValues = [1, 1, 1, 0.3, 0]
        self.expectedthrottleMod = []
        for idx in range(len(self.throttleAxisValues)):
            if self.throttleAxisValues[idx] >= self.testCtrlr._throttleFull \
                    and self.brakeAxisValues[idx] == self.testCtrlr._brakeOff:
                value = self.testCtrlr._throttleOff \
                    - self.throttleAxisValues[idx]
                throttleRange = self.testCtrlr._throttleFull \
                    - self.testCtrlr._throttleOff
                modifier = round(value / throttleRange, self.testCtrlr._ndigit)
                self.expectedthrottleMod.append(modifier)
            elif self.throttleAxisValues[idx] == self.testCtrlr._throttleOff \
                    and self.brakeAxisValues[idx] >= self.testCtrlr._brakeFull:
                value = self.testCtrlr._brakeOff \
                    - self.brakeAxisValues[idx]
                brakeRange = self.testCtrlr._brakeFull \
                    - self.testCtrlr._brakeOff
                modifier = -1 * round(value / brakeRange,
                                      self.testCtrlr._ndigit)
                self.expectedthrottleMod.append(modifier)
            else:
                self.expectedthrottleMod.append(0)

    def test_constructorInitJoystick(self):
        """
        The constructor must initialize the pygame joystick.
        """
        self.testJoysticks[0].reset_mock()
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch('pkgs.controller.joystick.Joystick') as mockedJoystick:
            mockedJoystick.return_value = self.testJoysticks[0]
            testCtrlr = Controller(self.testLogger,     # noqa: F841
                                   self.testIdxes[0], self.testNames[0])
            mockedJoystick.assert_called_once_with(self.testIdxes[0])
            self.testJoysticks[0].init.assert_called_once()

    def test_constructorLoadConfig(self):
        """
        The constructor must load the controller configuration.
        """
        expectedPath = os.path.join(Controller.CONFIG_ROOT_DIR,
                                    f"{self.testNames[0].replace(' ', '_')}.json")  # noqa: E501
        with patch('builtins.open', mock_open(read_data=self.testConfig)) \
                as mockedConfigFile, \
                patch('pkgs.controller.joystick.Joystick'):
            testCtrlr = Controller(self.testLogger,     # noqa: F841
                                   self.testIdxes[0], self.testNames[0])
            mockedConfigFile.assert_called_once_with(expectedPath)
            mockedConfigFile().read.assert_called_once()

    def test_listConnected(self):
        """
        The _listConnected mothod must return the list of
        connected controller name.
        """
        with patch('pkgs.controller.joystick') as mockJoystickMod:
            mockJoystickMod.get_count.return_value = len(self.testNames)
            mockJoystickMod.Joystick.side_effect = self.testJoysticks
            testResult = Controller._listConnected()
            self.assertEqual(testResult, self.testNames)

    def test_filterUnsupported(self):
        """
        The _filterUnsupported method must return a dictionnary containing
        only the supported and connected controller with the following struct:
            - key = controller name
            - value = joystick index
        """
        firstIdx = 0
        secondIdx = 2
        testSupported = (self.testNames[firstIdx].replace(' ', '_'),
                         self.testNames[secondIdx].replace(' ', '_'))
        expectedList = {}
        expectedList[self.testNames[firstIdx]] = self.testIdxes[firstIdx]
        expectedList[self.testNames[secondIdx]] = self.testIdxes[secondIdx]
        testResult = Controller._filterUnsupported(self.testNames,
                                                   testSupported)
        self.assertEqual(testResult, expectedList)

    def test_listControllerConncted(self):
        """
        The listController method must list the connected controller.
        """
        with patch.object(Controller, '_listConnected') \
                as mockedListConnected, \
                patch.object(Controller, '_filterUnsupported'), \
                patch('pkgs.controller.os.listdir'):
            Controller.listController()
            mockedListConnected.assert_called_once()

    def test_listControllerSupported(self):
        """
        The listController method must list the supported controller.
        """
        with patch.object(Controller, '_listConnected'), \
                patch.object(Controller, '_filterUnsupported'), \
                patch('pkgs.controller.os.listdir') as mockedListDir:
            Controller.listController()
            mockedListDir.assert_called_once_with(Controller.CONFIG_ROOT_DIR)

    def test_listControllerFilterUnsupported(self):
        """
        The listController method must filter the unsupported controllers.
        """
        testSupported = [f"{self.testNames[0].replace(' ', '_')}.json",
                         f"{self.testNames[2].replace(' ', '_')}.json"]
        expectedSupported = (f"{self.testNames[0].replace(' ', '_')}",
                             f"{self.testNames[2].replace(' ', '_')}")
        with patch.object(Controller, '_listConnected') \
                as mockedListConnected, \
                patch.object(Controller, '_filterUnsupported') \
                as mockedFilterUnsupported, \
                patch('pkgs.controller.os.listdir') as mockedListSupported:
            mockedListConnected.return_value = self.testNames
            mockedListSupported.return_value = testSupported
            Controller.listController()
            mockedFilterUnsupported.assert_called_once_with(self.testNames,
                                                            expectedSupported)

    def test_listController(self):
        """
        The listController method must return the list of
        available controller.
        """
        expectedList = {}
        expectedList[self.testNames[0]] = self.testIdxes[0]
        expectedList[self.testNames[2]] = self.testIdxes[2]
        with patch.object(Controller, '_listConnected'), \
                patch.object(Controller, '_filterUnsupported') \
                as mockedFilterUnsupported, \
                patch('pkgs.controller.os.listdir'):
            mockedFilterUnsupported.return_value = expectedList
            testResult = Controller.listController()
            self.assertEqual(testResult, expectedList)

    def test_saveSteeringLeft(self):
        """
        The _saveSteeringLeft must save the fully left steering axis.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('steering')
        expectedAxisValue = -0.97
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testCtrlr._saveSteeringLeft()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testCtrlr._steeringLeft,
                         abs(expectedAxisValue))

    def test_saveSteeringRight(self):
        """
        The _saveSteeringRight must save the fully right steering axis.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('steering')
        expectedAxisValue = -0.43
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testCtrlr._saveSteeringRight()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testCtrlr._steeringRight,
                         abs(expectedAxisValue))

    def test_saveThrottleOff(self):
        """
        The _saveThrottleOff must save the fully off throttle axis.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('throttle')
        expectedAxisValue = -0.27
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testCtrlr._saveThrottleOff()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testCtrlr._throttleOff,
                         abs(expectedAxisValue))

    def test_saveThrottleFull(self):
        """
        The _saveThrottleFull must save the fully on throttle axis.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('throttle')
        expectedAxisValue = -0.78
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testCtrlr._saveThrottleFull()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testCtrlr._throttleFull,
                         abs(expectedAxisValue))

    def test_saveBrakeOff(self):
        """
        The _saveBrakeOff must save the fully off brake axis.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('brake')
        expectedAxisValue = -0.10
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testCtrlr._saveBrakeOff()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testCtrlr._brakeOff,
                         abs(expectedAxisValue))

    def test_saveBrakeFull(self):
        """
        The _saveBrakeFull must save the fully on brake axis.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('brake')
        expectedAxisValue = -0.86
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testCtrlr._saveBrakeFull()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testCtrlr._brakeFull,
                         abs(expectedAxisValue))

    def test_getAxesMap(self):
        """
        The _getAxesMap method must return the controller axes mapping.
        """
        testResult = self.testCtrlr._getAxesMap()
        self.assertEqual(testResult,
                         self.testCtrlr._config[Controller.CTRLS_KEY][Controller.AXES_KEY])    # noqa: E501

    def test_getButtonsMap(self):
        """
        The _getButtonsMap method must return the controller buttons mapping.
        """
        testResult = self.testCtrlr._getButtonsMap()
        self.assertEqual(testResult,
                         self.testCtrlr._config[Controller.CTRLS_KEY][Controller.BTNS_KEY])    # noqa: E501

    def test_getHatsMap(self):
        """
        The _getHatsMap method must return the controller hats mapping.
        """
        testResult = self.testCtrlr._getHatsMap()
        self.assertEqual(testResult,
                         self.testCtrlr._config[Controller.CTRLS_KEY][Controller.HATS_KEY])    # noqa: E501

    def test_getFuncMap(self):
        """
        The _getFuncMap method must return the controller functions mapping.
        """
        testResult = self.testCtrlr._getFuncMap()
        self.assertEqual(testResult,
                         self.testCtrlr._config[Controller.FUNC_KEY])

    def test_getSterringModifier(self):
        """
        The getSterringModifier must return the sterring modifer.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index('steering')
        for idx, value in enumerate(self.steeringAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testCtrlr.getSteeringModifier()
            self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)     # noqa: E501
            self.testJoysticks[0].get_axis.reset_mock()
            self.assertEqual(testResult, self.expectedSteeringMod[idx])
