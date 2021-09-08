from unittest import TestCase
from unittest.mock import Mock, mock_open, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.unit import Unit      # noqa: E402


class TestUnit(TestCase):
    """
    The Unit class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.testUnitId = 'test unit 1'
        self.testLogging = Mock()
        self.testLogger = Mock()
        self.testClient = Mock()
        self.testMsg = Mock()
        with patch('pkgs.unit.UnitWhldCmdMsg') as mockedUnitWhldCmdMsg:
            mockedUnitWhldCmdMsg.return_value = self.testMsg
            self.testLogging.getLogger.return_value = self.testLogger
            self.testUnit = Unit(self.testLogging, self.testClient,
                                 self.testUnitId)
        self.testLogging.getLogger.reset_mock()

    def test_contructor(self):
        """
        The constructor must save its initialization data and initialize
        its logger.
        """
        testId = 'test unit'
        with patch('pkgs.unit.UnitWhldCmdMsg') as mockedUnitWhledCmdMsg:
            testUnit = Unit(self.testLogging, self.testClient, testId)
            self.testLogging.getLogger.assert_called_once_with(f"UNIT-{testId.upper()}")    # noqa: E501
            self.assertEqual(testUnit._id, testId)
            self.assertEqual(testUnit._client, self.testClient)
            mockedUnitWhledCmdMsg.assert_called_once_with(testId)

    def test_combineThrtlBrakeThrtlActive(self):
        """
        The _combineThrlBrake must generate the throttle command base
        from the throttle modifier if only the throttle is active.
        """
        expectedThrtlMod = 0.54
        brakeModifier = 0.0
        testResult = self.testUnit._combineThrtlBrake(expectedThrtlMod,
                                                      brakeModifier)
        self.assertEqual(testResult, expectedThrtlMod)

    def test_combineThrtlBrakeBrakeActive(self):
        """
        The _combineThrlBrake must generate the throttle command base
        from the brake modifier * -1 if only the brake is active.
        """
        throttleModifier = 0.0
        expectedBrakeMod = 0.99
        testResult = self.testUnit._combineThrtlBrake(throttleModifier,
                                                      expectedBrakeMod)
        self.assertEqual(testResult, expectedBrakeMod * -1)

    def test_combineThrtlBrakeZeroMod(self):
        """
        The _combineThrlBrake must set the throttle command to 0 if
        both the throttle and the brake are inactive or active.
        """
        throttleModifiers = [0.0, 0.56]
        brakeModifiers = [0.0, 0.12]
        for idx in range(len(throttleModifiers)):
            testResult = self.testUnit._combineThrtlBrake(throttleModifiers[idx],   # noqa: E501
                                                          brakeModifiers[idx])
            self.assertEqual(testResult, 0.0)

    def test_getId(self):
        """
        The getId method must return the unit id.
        """
        testResult = self.testUnit.getId()
        self.assertEqual(testResult, self.testUnitId)

    def test_updateSteeringCmd(self):
        """
        The updateSteeringCmd must update the steering modifier in
        the next command message.
        """
        expectedModifier = -0.12
        self.testUnit.updateSteeringCmd(expectedModifier)
        self.testMsg.setSteering.assert_called_once_with(expectedModifier)
        self.testClient.publish.assert_not_called()
