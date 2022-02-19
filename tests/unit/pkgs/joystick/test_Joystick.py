from typing import Callable
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
        self.threadPoolClass = 'pkgs.joystick.joystick.QThreadPool'
        self.threadPoolMock = Mock()
        self.timerClass = 'pkgs.joystick.joystick.QTimer'
        self.mockedTimer = Mock()
        self.joystickClass = 'pkgs.joystick.joystick.joystick.Joystick'
        self.joystickProcessorClass = \
            'pkgs.joystick.joystick.JoystickProcessor'
        self.mockedProcessor = Mock()
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
        self.testJoystick._threadPool = self.threadPoolMock
        self.testJoystick._processTimer = self.mockedTimer

    def test_constructorInitJoystick(self):
        """
        The constructor must initialize the pygame joystick.
        """
        self.testJoysticks[0].reset_mock()
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch(self.joystickClass) as mockedJoystick, \
                patch.object(Joystick, '_setupProcessor'):
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
                as mockedConfigFile, patch(self.joystickClass), \
                patch.object(Joystick, '_setupProcessor'):
            Joystick(self.testLogger, self.testIdxes[0], self.testNames[0])
            mockedConfigFile.assert_called_once_with(expectedPath)
            mockedConfigFile().read.assert_called_once()

    def test_constructorSetupProcessor(self):
        """
        The constructor must setup the joystick's processor.
        """
        with patch('builtins.open', mock_open(read_data=self.testConfig)), \
                patch(self.joystickClass), \
                patch.object(Joystick, '_setupProcessor') as mockedSetuProc:
            Joystick(self.testLogger, self.testIdxes[0], self.testNames[0])
            mockedSetuProc.assert_called_once()

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

    def test_calculateModifier(self):
        """
        The _calculateModifier method must calculate the modifier value
        based on the passed min, max and actual value.
        """
        testValSets = (
            {'limits': {'min': -1.75, 'max': 1.75}, 'val': -0.6, 'result': -0.34},  # noqa: E501
            {'limits': {'min': -1.75, 'max': 1.75}, 'val': 1.1, 'result': 0.63},    # noqa: E501
            {'limits': {'min': 0, 'max': 1.25}, 'val': 0.65, 'result': 0.52},
            {'limits': {'min': 1.25, 'max': 2.0}, 'val': 1.99, 'result': 0.99},
        )
        for valSet in testValSets:
            self.assertEqual(self.testJoystick
                             ._calculateModifier(valSet['limits'],
                                                 valSet['val']),
                             valSet['result'])

    def test_processAxisSignal(self):
        """
        The _processAxisSignal method must emit the axis motion signal
        with the axis modifier only when the joystick is calibrated.
        """
        expectedType = self.testJoystick._config[Joystick.TYPE_KEY]
        expectedMod = 0.2
        testPosition = 0.4
        testCalibStates = [False, True]
        with patch.object(self.testJoystick, 'axisMotion') as mockedSignals, \
                patch.object(self.testJoystick, '_calculateModifier') \
                as mockedCalcMod:
            for calibState in testCalibStates:
                mockedCalcMod.return_value = expectedMod
                self.testJoystick._isCalibrated = calibState
                self.testJoystick._processAxisSignal(self.testIdxes[0],
                                                     testPosition)
            mockedCalcMod.assert_called_once_with(self.testJoystick._axes[0],
                                                  testPosition)
            mockedSignals.emit.assert_called_once_with(expectedType,
                                                       self.testIdxes[0],
                                                       expectedMod)

    def test_processBtnDownSignal(self):
        """
        The _processBtnDownSignal method must emit the button down
        signal.
        """
        expectedType = self.testJoystick._config[Joystick.TYPE_KEY]
        with patch.object(self.testJoystick, 'buttonDown') as mockedSignals:
            self.testJoystick._processBtnDownSignal(self.testIdxes[0])
            mockedSignals.emit.assert_called_once_with(expectedType,
                                                       self.testIdxes[0])

    def test_processBtnUpSignal(self):
        """
        The _processBtnUpSignal method must emit the button up
        signal.
        """
        expectedType = self.testJoystick._config[Joystick.TYPE_KEY]
        with patch.object(self.testJoystick, 'buttonUp') as mockedSignals:
            self.testJoystick._processBtnUpSignal(self.testIdxes[0])
            mockedSignals.emit.assert_called_once_with(expectedType,
                                                       self.testIdxes[0])

    def test_processHatSignal(self):
        """
        The _processHatSignal method must emit the axis motion signal
        with the axis modifier.
        """
        expectedType = self.testJoystick._config[Joystick.TYPE_KEY]
        testPosition = (1, -1)
        with patch.object(self.testJoystick, 'hatMotion') as mockedSignals:
            self.testJoystick._processHatSignal(self.testIdxes[0],
                                                testPosition)
            mockedSignals.emit.assert_called_once_with(expectedType,
                                                       self.testIdxes[0],
                                                       testPosition)

    def test_startProcessingWorker(self):
        """
        The _startProcessing method must create the worker and
        connect to its signals.
        """
        with patch(self.joystickProcessorClass) as mockedProc:
            mockedProc.return_value = self.mockedProcessor
            self.testJoystick._startProcessing()
            axisArgs, _ = \
                self.mockedProcessor.signals.axisMotion.connect.call_args
            self.assertTrue(isinstance(axisArgs[0], Callable))
            axisArgs, _ = \
                self.mockedProcessor.signals.hatMotion.connect.call_args
            self.assertTrue(isinstance(axisArgs[0], Callable))
            axisArgs, _ = \
                self.mockedProcessor.signals.buttonDown.connect.call_args
            self.assertTrue(isinstance(axisArgs[0], Callable))
            axisArgs, _ = \
                self.mockedProcessor.signals.buttonUp.connect.call_args
            self.assertTrue(isinstance(axisArgs[0], Callable))

    def test_startProcessingStartWorker(self):
        """
        The _startProcessing method must start the processing worker.
        """
        with patch(self.joystickProcessorClass) as mockedProc:
            mockedProc.return_value = self.mockedProcessor
            self.testJoystick._startProcessing()
            self.testJoystick._threadPool.start \
                .assert_called_once_with(self.mockedProcessor)

    def test_setupProcessorThreadPool(self):
        """
        The _setupProcessor must get the thread pool instance.
        """
        with patch(self.threadPoolClass) as mockedThread, \
                patch(self.joystickProcessorClass), \
                patch(self.timerClass):
            self.testJoystick._setupProcessor()
            mockedThread.globalInstance.assert_called_once()

    def test_setupProcessorTimer(self):
        """
        The _setupProcessor method must create the timer and
        connect to its timeout signal.
        """
        with patch(self.threadPoolClass), \
                patch(self.timerClass) as mockedTimer:
            mockedTimer.return_value = self.mockedTimer
            self.testJoystick._setupProcessor()
            timeoutArgs, _ = \
                self.mockedTimer.timeout.connect.call_args
            self.assertTrue(isinstance(timeoutArgs[0], Callable))

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

    def test_activate(self):
        """
        The activate method must start the processor timer.
        """
        self.testJoystick.activate()
        self.mockedTimer.start. \
            assert_called_once_with(self.testJoystick.FRAME_PERIOD_MS)

    def test_deactivate(self):
        """
        The deactivate method must stop the processor timer.
        """
        self.testJoystick.deactivate()
        self.mockedTimer.stop \
            .assert_called_once()

    def test_calibrateAlreadyDone(self):
        """
        The calibrate method must do nothing if the joystick
        is already calibrated.
        """
        self.testJoystick._isCalibrated = True
        expectedCalibSeq = self.testJoystick._calibSeq
        with patch.object(self.testJoystick, 'calibration') as mockedCalib:
            self.testJoystick.calibrate()
            self.testJoystick._joystick.get_axis.assert_not_called()
            mockedCalib.assert_not_called()
            self.assertEqual(self.testJoystick._calibSeq, expectedCalibSeq)

    def test_calibrateEmitSeqMngmt(self):
        """
        The calibrate method must emit the current sequence message,
        increment the calibration seq, and reset it and set the calibration
        flag when calibration is done.
        """
        for seq in self.testJoystick._config[Joystick.CALIB_KEY]:
            with patch.object(self.testJoystick, 'calibration') as mockedCalib:
                self.testJoystick.calibrate()
                mockedCalib.emit.assert_called_once_with(seq['msg'])
        self.assertTrue(self.testJoystick._isCalibrated)

    def test_calibrateSaveAxesMinMax(self):
        """
        The calibrate method must save the minimum and maximum of the axes.
        """
        axesPos = (-1.5, 1.5, 0, 1.32, 0.75, 1.45)
        self.testJoystick._joystick.get_axis.side_effect = axesPos
        self.testJoystick._joystick.get_axis.side_effect = axesPos
        for idx, seq in enumerate(self.testJoystick._config[Joystick.CALIB_KEY]):       # noqa: E501
            with patch.object(self.testJoystick, 'calibration'):
                self.testJoystick.calibrate()
            if 'axis' in seq:
                self.testJoystick._joystick.get_axis.assert_called_with(seq['axis'])    # noqa: E501
                self.assertEqual(self.testJoystick._axes[seq['axis']][seq['limit']],    # noqa: E501
                                 axesPos[idx - 1])

    def test_isCalibrated(self):
        """
        The isCalibrated method must return the calibration status.
        """
        expectedStates = (True, False)
        for expectedState in expectedStates:
            self.testJoystick._isCalibrated = expectedState
            if expectedState:
                self.assertTrue(self.testJoystick.isCalibrated())
            else:
                self.assertFalse(self.testJoystick.isCalibrated())

    def test_quit(self):
        """
        The quit method must call the quit method of its joystick.
        """
        self.testJoystick.quit()
        self.testJoysticks[0].quit.assert_called_once()
