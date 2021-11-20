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
        self.testRoot = Mock()
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
            self.testCtrlr = Controller(self.testRoot, self.testLogger,
                                        0, self.testNames[0])
        self._setSteeringValues()
        self._setThrottleValues()
        self._setBrakeValues()

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
        self.throttleAxisValues = [1, 0.835, 0.245, 0]
        self.expectedThrottleMod = []
        for value in self.throttleAxisValues:
            tmpVal = self.testCtrlr._throttleOff - value
            throttleRange = self.testCtrlr._throttleOff \
                - self.testCtrlr._throttleFull
            modifier = round(tmpVal / throttleRange, self.testCtrlr._ndigit)
            self.expectedThrottleMod.append(modifier)

    def _setBrakeValues(self):
        """
        Set the test controller brake test values.
        """
        self.testCtrlr._brakeOff = 1
        self.testCtrlr._brakeFull = 0
        self.brakeAxisValues = [1.000, 0.727, 0.352, 0.000]
        self.expectedBrakeMod = []
        for value in self.brakeAxisValues:
            tmpVal = self.testCtrlr._brakeOff - value
            brakeRange = self.testCtrlr._brakeOff - self.testCtrlr._brakeFull
            modifier = round(tmpVal / brakeRange, self.testCtrlr._ndigit)
            self.expectedBrakeMod.append(modifier)

    def test_constructorInitJoystick(self):
        """
        The constructor must initialize the pygame joystick.
        """
        self.testJoysticks[0].reset_mock()
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch('pkgs.controller.joystick.Joystick') as mockedJoystick:
            mockedJoystick.return_value = self.testJoysticks[0]
            testCtrlr = Controller(self.testRoot, self.testLogger,  # noqa: F841 E501
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
            testCtrlr = Controller(self.testRoot, self.testLogger,  # noqa: F841 E501
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
            Controller.listControllers()
            mockedListConnected.assert_called_once()

    def test_listControllerSupported(self):
        """
        The listController method must list the supported controller.
        """
        with patch.object(Controller, '_listConnected'), \
                patch.object(Controller, '_filterUnsupported'), \
                patch('pkgs.controller.os.listdir') as mockedListDir:
            Controller.listControllers()
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
            Controller.listControllers()
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
            testResult = Controller.listControllers()
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
        The _getSterringModifier must return the sterring modifer.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index(Controller.STRG_KEY)       # noqa: E501
        for idx, value in enumerate(self.steeringAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testCtrlr._getSteeringModifier()
            self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)     # noqa: E501
            self.testJoysticks[0].get_axis.reset_mock()
            self.assertEqual(testResult, self.expectedSteeringMod[idx])

    def test_getThrottleModifier(self):
        """
        The _getThrottleModifier must return the throttle modifier.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index(Controller.THRTL_KEY)      # noqa: E501
        for idx, value in enumerate(self.throttleAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testCtrlr._getThrottleModifier()
            self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)     # noqa: E501
            self.testJoysticks[0].get_axis.reset_mock()
            self.assertEqual(testResult, self.expectedThrottleMod[idx])

    def test_getBrakeModifier(self):
        """
        The _getBrakeModifier must return the brake modifier.
        """
        expectedAxisIdx = self.testCtrlr._getAxesMap().index(Controller.BRK_KEY)        # noqa: E501
        for idx, value in enumerate(self.brakeAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testCtrlr._getBrakeModifier()
            self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)     # noqa: E501
            self.testJoysticks[0].get_axis.reset_mock()
            self.assertEqual(testResult, self.expectedBrakeMod[idx])

    def test_calibrateSaveStrgLeft(self):
        """
        The calibrate method must save the steering left calibration
        value when the calibration sequence is 0 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 0
        with patch.object(self.testCtrlr, '_saveSteeringLeft') \
                as mockedSave:
            self.testCtrlr._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveStrgRight(self):
        """
        The _calibrate method must save the steering right calibration
        value when the calibration sequence is 1 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 1
        with patch.object(self.testCtrlr, '_saveSteeringRight') \
                as mockedSave:
            self.testCtrlr._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveThrtlOff(self):
        """
        The _calibrate method must save the throttle off calibration
        value when the calibration sequence is 2 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 2
        with patch.object(self.testCtrlr, '_saveThrottleOff') \
                as mockedSave:
            self.testCtrlr._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveThrtlFull(self):
        """
        The _calibrate method must save the throttle full calibration
        value when the calibration sequence is 3 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 3
        with patch.object(self.testCtrlr, '_saveThrottleFull') \
                as mockedSave:
            self.testCtrlr._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveBrkOff(self):
        """
        The _calibrate method must save the brake off calibration
        value when the calibration sequence is 4 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 4
        with patch.object(self.testCtrlr, '_saveBrakeOff') \
                as mockedSave:
            self.testCtrlr._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveBrkFull(self):
        """
        The _calibrate method must save the brake full calibration
        value when the calibration sequence is 5 and set the _isCalibratedFlag
        to true.
        """
        testCalibSeqNumber = 5
        with patch.object(self.testCtrlr, '_saveBrakeFull') \
                as mockedSave:
            self.testCtrlr._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()
            self.assertTrue(self.testCtrlr._isCalibrated)

    def test_getName(self):
        """
        The getName method must return the controller name.
        """
        expectedName = 'test joystick'
        self.testJoysticks[0].get_name.return_value = expectedName
        testResult = self.testCtrlr.getName()
        self.assertEqual(testResult, expectedName)

    def test_getIdx(self):
        """
        The getIdx method must return the controller index.
        """
        testResult = self.testCtrlr.getIdx()
        self.assertEqual(testResult, self.testIdxes[0])

    def test_getType(self):
        """
        The getType method must return the controller type.
        """
        testResult = self.testCtrlr.getType()
        self.assertEqual(testResult,
                         self.testCtrlr._config[Controller.TYPE_KEY])

    def test_processEventsNotCalibrated(self):
        """
        The processEvents method must not process event if not calibrated.
        """
        with patch('pkgs.controller.event') as mockedEvent:
            self.testCtrlr.processEvents()
            mockedEvent.get.assert_not_called()

    def test_processEventPygameEvent(self):
        """
        The processEvents method must fetch the pygame events.
        """
        self.testCtrlr._isCalibrated = True
        with patch('pkgs.controller.event') as mockedEvent:
            print(mockedEvent)
            mockedEvent.return_value = []
            self.testCtrlr.processEvents()
            mockedEvent.get.assert_called_once()

    def test_quit(self):
        """
        The quit method must call the quit method of its joystick.
        """
        self.testCtrlr.quit()
        self.testJoysticks[0].quit.assert_called_once()
