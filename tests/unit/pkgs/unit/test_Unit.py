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

    def test_getId(self):
        """
        The getId method must return the unit id.
        """
        testResult = self.testUnit.getId()
        self.assertEqual(testResult, self.testUnitId)
