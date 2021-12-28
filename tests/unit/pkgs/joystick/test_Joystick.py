from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.joystick.joystick import Joystick  # noqa: E402


class TestJoystick(TestCase):
    """
    The Joystick class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.pygamePkg = 'pkgs.joystick.joystick.pg'
        self.joystickClass = 'pkgs.joystick.joystick.joystick.Joystick'
        self.testLogger = Mock()
        self.testNames = ('test ctrlr 1', 'test ctrlr 2', 'test ctrlr 3')
        self.testIdxes = (0, 1, 2)
        self.testJoysticks = []
        for idx in range(len(self.testNames)):
            mockedJoystick = Mock()
            mockedJoystick.get_name.return_value = self.testNames[idx]
            self.testJoysticks.append(mockedJoystick)
        with open('src/pkgs/joystick/configs/logitech_driving_force.json') \
                as configFile:
            self.testConfig = configFile.read()
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch(self.joystickClass) as mockedJoystick:
            mockedJoystick.return_value = self.testJoysticks[0]
            self.testJoystick = Joystick(self.testLogger, 0, self.testNames[0])
        self._setSteeringValues()
        self._setThrottleValues()
        self._setBrakeValues()

    def _setSteeringValues(self):
        """
        Set the test joystick steering axis test values.
        """
        self.testJoystick._steeringLeft = 1
        self.testJoystick._steeringRight = 1
        self.steeringAxisValues = [-1, -0.5, 0, 0.25, 1]
        self.expectedSteeringMod = []
        for value in self.steeringAxisValues:
            if value < 0:
                modifier = round(value / self.testJoystick._steeringLeft,
                                 self.testJoystick._ndigit)
                self.expectedSteeringMod.append(modifier)
            else:
                modifier = round(value / self.testJoystick._steeringRight,
                                 self.testJoystick._ndigit)
                self.expectedSteeringMod.append(modifier)

    def _setThrottleValues(self):
        """
        Set the test joystick throttle/brake axis test values.
        """
        self.testJoystick._throttleOff = 1
        self.testJoystick._throttleFull = 0
        self.throttleAxisValues = [1, 0.835, 0.245, 0]
        self.expectedThrottleMod = []
        for value in self.throttleAxisValues:
            tmpVal = self.testJoystick._throttleOff - value
            throttleRange = self.testJoystick._throttleOff \
                - self.testJoystick._throttleFull
            modifier = round(tmpVal / throttleRange, self.testJoystick._ndigit)
            self.expectedThrottleMod.append(modifier)

    def _setBrakeValues(self):
        """
        Set the test joystick brake test values.
        """
        self.testJoystick._brakeOff = 1
        self.testJoystick._brakeFull = 0
        self.brakeAxisValues = [1.000, 0.727, 0.352, 0.000]
        self.expectedBrakeMod = []
        for value in self.brakeAxisValues:
            tmpVal = self.testJoystick._brakeOff - value
            brakeRange = self.testJoystick._brakeOff - \
                self.testJoystick._brakeFull
            modifier = round(tmpVal / brakeRange, self.testJoystick._ndigit)
            self.expectedBrakeMod.append(modifier)

    def test_constructorInitJoystick(self):
        """
        The constructor must initialize the pygame joystick.
        """
        self.testJoysticks[0].reset_mock()
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch(self.joystickClass) \
                as mockedJoystick:
            mockedJoystick.return_value = self.testJoysticks[0]
            Joystick(self.testLogger, self.testIdxes[0], self.testNames[0])
            mockedJoystick.assert_called_once_with(self.testIdxes[0])
            self.testJoysticks[0].init.assert_called_once()

    def test_constructorLoadConfig(self):
        """
        The constructor must load the joystick configuration.
        """
        expectedPath = os.path.join(Joystick.CONFIG_ROOT_DIR,
                                    f"{self.testNames[0].replace(' ', '_')}.json")  # noqa: E501
        with patch('builtins.open', mock_open(read_data=self.testConfig)) \
                as mockedConfigFile, \
                patch(self.joystickClass):
            Joystick(self.testLogger, self.testIdxes[0], self.testNames[0])
            mockedConfigFile.assert_called_once_with(expectedPath)
            mockedConfigFile().read.assert_called_once()

    def test_initFramework(self):
        """
        The initFramework method must initialize the pygame framework.
        """
        with patch(self.pygamePkg) as mockedPygame:
            mockedPygame.JOYAXISMOTION = 0
            mockedPygame.JOYBUTTONDOWN = 1
            mockedPygame.JOYBUTTONUP = 2,
            mockedPygame.JOYHATMOTION = 3
            expectedEvents = [mockedPygame.JOYAXISMOTION,
                              mockedPygame.JOYBUTTONDOWN,
                              mockedPygame.JOYBUTTONUP,
                              mockedPygame.JOYHATMOTION]
            Joystick.initFramework()
            mockedPygame.init.assert_called_once()
            mockedPygame.event.set_allowed.assert_called_once_with(expectedEvents)  # noqa: E501

    def test_listConnected(self):
        """
        The _listConnected mothod must return the list of
        connected joystick name.
        """
        with patch('pkgs.joystick.joystick.joystick') as mockJoystickMod:
            mockJoystickMod.get_count.return_value = len(self.testNames)
            mockJoystickMod.Joystick.side_effect = self.testJoysticks
            testResult = Joystick._listConnected()
            self.assertEqual(testResult, self.testNames)

    def test_filterUnsupported(self):
        """
        The _filterUnsupported method must return a dictionnary containing
        only the supported and connected joystick with the following struct:
            - key = joystick name
            - value = joystick index
        """
        firstIdx = 0
        secondIdx = 2
        testSupported = (self.testNames[firstIdx].replace(' ', '_'),
                         self.testNames[secondIdx].replace(' ', '_'))
        expectedList = {}
        expectedList[self.testNames[firstIdx]] = self.testIdxes[firstIdx]
        expectedList[self.testNames[secondIdx]] = self.testIdxes[secondIdx]
        testResult = Joystick._filterUnsupported(self.testNames,
                                                 testSupported)
        self.assertEqual(testResult, expectedList)

    def test_listAvailableConnected(self):
        """
        The listAvailable method must list the connected joystick.
        """
        with patch.object(Joystick, '_listConnected') \
                as mockedListConnected, \
                patch.object(Joystick, '_filterUnsupported'), \
                patch('pkgs.joystick.joystick.os.listdir'):
            Joystick.listAvailable()
            mockedListConnected.assert_called_once()

    def test_listAvailableSupported(self):
        """
        The listAvailable method must list the supported joystick.
        """
        with patch.object(Joystick, '_listConnected'), \
                patch.object(Joystick, '_filterUnsupported'), \
                patch('pkgs.joystick.joystick.os.listdir') as mockedListDir:    # noqa: E501
            Joystick.listAvailable()
            mockedListDir.assert_called_once_with(Joystick.CONFIG_ROOT_DIR)

    def test_listAvailableFilterUnsupported(self):
        """
        The listAvailable method must filter the unsupported joystick.
        """
        testSupported = [f"{self.testNames[0].replace(' ', '_')}.json",
                         f"{self.testNames[2].replace(' ', '_')}.json"]
        expectedSupported = (f"{self.testNames[0].replace(' ', '_')}",
                             f"{self.testNames[2].replace(' ', '_')}")
        with patch.object(Joystick, '_listConnected') \
                as mockedListConnected, \
                patch.object(Joystick, '_filterUnsupported') \
                as mockedFilterUnsupported, \
                patch('pkgs.joystick.joystick.os.listdir') as mockedListSupported:  # noqa: E501
            mockedListConnected.return_value = self.testNames
            mockedListSupported.return_value = testSupported
            Joystick.listAvailable()
            mockedFilterUnsupported.assert_called_once_with(self.testNames,
                                                            expectedSupported)

    def test_listAvailable(self):
        """
        The listAvailable method must return the list of
        available joystick.
        """
        expectedList = {}
        expectedList[self.testNames[0]] = self.testIdxes[0]
        expectedList[self.testNames[2]] = self.testIdxes[2]
        with patch.object(Joystick, '_listConnected'), \
                patch.object(Joystick, '_filterUnsupported') \
                as mockedFilterUnsupported, \
                patch('pkgs.joystick.joystick.os.listdir'):
            mockedFilterUnsupported.return_value = expectedList
            testResult = Joystick.listAvailable()
            self.assertEqual(testResult, expectedList)

    def test_saveSteeringLeft(self):
        """
        The _saveSteeringLeft must save the fully left steering axis.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index('steering')
        expectedAxisValue = -0.97
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testJoystick._saveSteeringLeft()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testJoystick._steeringLeft,
                         abs(expectedAxisValue))

    def test_saveSteeringRight(self):
        """
        The _saveSteeringRight must save the fully right steering axis.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index('steering')
        expectedAxisValue = -0.43
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testJoystick._saveSteeringRight()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testJoystick._steeringRight,
                         abs(expectedAxisValue))

    def test_saveThrottleOff(self):
        """
        The _saveThrottleOff must save the fully off throttle axis.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index('throttle')
        expectedAxisValue = -0.27
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testJoystick._saveThrottleOff()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testJoystick._throttleOff,
                         abs(expectedAxisValue))

    def test_saveThrottleFull(self):
        """
        The _saveThrottleFull must save the fully on throttle axis.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index('throttle')
        expectedAxisValue = -0.78
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testJoystick._saveThrottleFull()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testJoystick._throttleFull,
                         abs(expectedAxisValue))

    def test_saveBrakeOff(self):
        """
        The _saveBrakeOff must save the fully off brake axis.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index('brake')
        expectedAxisValue = -0.10
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testJoystick._saveBrakeOff()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testJoystick._brakeOff,
                         abs(expectedAxisValue))

    def test_saveBrakeFull(self):
        """
        The _saveBrakeFull must save the fully on brake axis.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index('brake')
        expectedAxisValue = -0.86
        self.testJoysticks[0].get_axis.return_value = expectedAxisValue
        self.testJoystick._saveBrakeFull()
        self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)
        self.assertEqual(self.testJoystick._brakeFull,
                         abs(expectedAxisValue))

    def test_getAxesMap(self):
        """
        The _getAxesMap method must return the joystick axes mapping.
        """
        testResult = self.testJoystick._getAxesMap()
        self.assertEqual(testResult,
                         self.testJoystick._config[Joystick.CTRLS_KEY][Joystick.AXES_KEY])    # noqa: E501

    def test_getButtonsMap(self):
        """
        The _getButtonsMap method must return the joystick buttons mapping.
        """
        testResult = self.testJoystick._getButtonsMap()
        self.assertEqual(testResult,
                         self.testJoystick._config[Joystick.CTRLS_KEY][Joystick.BTNS_KEY])    # noqa: E501

    def test_getHatsMap(self):
        """
        The _getHatsMap method must return the joystick hats mapping.
        """
        testResult = self.testJoystick._getHatsMap()
        self.assertEqual(testResult,
                         self.testJoystick._config[Joystick.CTRLS_KEY][Joystick.HATS_KEY])    # noqa: E501

    def test_getFuncMap(self):
        """
        The _getFuncMap method must return the joystick functions mapping.
        """
        testResult = self.testJoystick._getFuncMap()
        self.assertEqual(testResult,
                         self.testJoystick._config[Joystick.FUNC_KEY])

    def test_getSterringModifier(self):
        """
        The _getSterringModifier must return the sterring modifer.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index(Joystick.STRG_KEY)       # noqa: E501
        for idx, value in enumerate(self.steeringAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testJoystick._getSteeringModifier()
            self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)     # noqa: E501
            self.testJoysticks[0].get_axis.reset_mock()
            self.assertEqual(testResult, self.expectedSteeringMod[idx])

    def test_getThrottleModifier(self):
        """
        The _getThrottleModifier must return the throttle modifier.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index(Joystick.THRTL_KEY)      # noqa: E501
        for idx, value in enumerate(self.throttleAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testJoystick._getThrottleModifier()
            self.testJoysticks[0].get_axis.assert_called_once_with(expectedAxisIdx)     # noqa: E501
            self.testJoysticks[0].get_axis.reset_mock()
            self.assertEqual(testResult, self.expectedThrottleMod[idx])

    def test_getBrakeModifier(self):
        """
        The _getBrakeModifier must return the brake modifier.
        """
        expectedAxisIdx = self.testJoystick._getAxesMap().index(Joystick.BRK_KEY)        # noqa: E501
        for idx, value in enumerate(self.brakeAxisValues):
            self.testJoysticks[0].get_axis.return_value = value
            testResult = self.testJoystick._getBrakeModifier()
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
        with patch.object(self.testJoystick, '_saveSteeringLeft') \
                as mockedSave:
            self.testJoystick._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveStrgRight(self):
        """
        The _calibrate method must save the steering right calibration
        value when the calibration sequence is 1 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 1
        with patch.object(self.testJoystick, '_saveSteeringRight') \
                as mockedSave:
            self.testJoystick._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveThrtlOff(self):
        """
        The _calibrate method must save the throttle off calibration
        value when the calibration sequence is 2 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 2
        with patch.object(self.testJoystick, '_saveThrottleOff') \
                as mockedSave:
            self.testJoystick._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveThrtlFull(self):
        """
        The _calibrate method must save the throttle full calibration
        value when the calibration sequence is 3 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 3
        with patch.object(self.testJoystick, '_saveThrottleFull') \
                as mockedSave:
            self.testJoystick._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveBrkOff(self):
        """
        The _calibrate method must save the brake off calibration
        value when the calibration sequence is 4 and advance to the
        next sequence.
        """
        testCalibSeqNumber = 4
        with patch.object(self.testJoystick, '_saveBrakeOff') \
                as mockedSave:
            self.testJoystick._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()

    def test_calibrateSaveBrkFull(self):
        """
        The _calibrate method must save the brake full calibration
        value when the calibration sequence is 5 and set the _isCalibratedFlag
        to true.
        """
        testCalibSeqNumber = 5
        with patch.object(self.testJoystick, '_saveBrakeFull') \
                as mockedSave:
            self.testJoystick._calibrate(testCalibSeqNumber)
            mockedSave.assert_called_once()
            self.assertTrue(self.testJoystick._isCalibrated)

    def test_getName(self):
        """
        The getName method must return the joystick name.
        """
        expectedName = 'test joystick'
        self.testJoysticks[0].get_name.return_value = expectedName
        testResult = self.testJoystick.getName()
        self.assertEqual(testResult, expectedName)

    def test_getIdx(self):
        """
        The getIdx method must return the joystick index.
        """
        testResult = self.testJoystick.getIdx()
        self.assertEqual(testResult, self.testIdxes[0])

    def test_getType(self):
        """
        The getType method must return the joystick type.
        """
        testResult = self.testJoystick.getType()
        self.assertEqual(testResult,
                         self.testJoystick._config[Joystick.TYPE_KEY])

    def test_quit(self):
        """
        The quit method must call the quit method of its joystick.
        """
        self.testJoystick.quit()
        self.testJoysticks[0].quit.assert_called_once()
