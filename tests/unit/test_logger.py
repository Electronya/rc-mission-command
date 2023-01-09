from argparse import Namespace
from copy import deepcopy
from unittest import TestCase
from unittest.mock import call, Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

import logger as dut                    # noqa: E402
from logger import _loggingSettings     # noqa: E402


class TestLogger(TestCase):
    """
    The logger test cases.
    """
    def setUp(self) -> None:
        self.loggingConfig = 'logger.logging.config'
        self.argparsePkg = 'logger.argparse'
        self.loggingMod = 'logger.logging'
        self.appCmpts = ['app', 'app.composer', 'app.windows.main',
                         'app.windows.ctrlr', 'app.windows.ctrlr.model']
        self.testArg = Namespace()
        self.testArg.app = None

    def test_getAppCmptNames(self) -> None:
        """
        The _getAppCmptNames function must return the supported
        application component names.
        """
        expectedRes = ['app', 'app.composer', 'app.windows.main',
                       'app.windows.ctrlr', 'app.windows.ctrlr.model']
        testResult = dut._getAppCmptNames()
        self.assertEqual(testResult, expectedRes, '_getAppCmptNames failed '
                         'to return the supported app component names.')

    def test_parseArgumentsParserSetup(self) -> None:
        """
        The _parseArguments function must setup the parser.
        """
        options = [{'short': '-a', 'long': '--app',
                    'help': f"Set debug level for application components."
                    f"\nUse the following component names : {self.appCmpts}."},
                   {'short': '-j', 'long': '--joy',
                    'help': 'Set debug level for joystick controller.'
                    '\nUse <joysticks.[index number]>.'}]
        expectedCalls = []
        for option in options:
            expectedCalls.append(call(option['short'], option['long'],
                                      type=str, default=None,
                                      help=option['help']))
        mockedParser = Mock()
        with patch(self.argparsePkg) as mockedArgParsePkg, \
                patch('logger._getAppCmptNames') as mockedGetAppCmptNames:
            mockedArgParsePkg.ArgumentParser.return_value = mockedParser
            mockedGetAppCmptNames.return_value = self.appCmpts
            dut._parseArguments()
            mockedArgParsePkg.ArgumentParser.assert_called_once()
            mockedParser.add_argument.assert_has_calls(expectedCalls)

    def test_parseArgumentsParserReturnParsedArg(self) -> None:
        """
        The _parseArguments function must return the parsed arguments.
        """
        mockedParser = Mock()
        expectedResult = Namespace()
        with patch(self.argparsePkg) as mockedArgParsePkg, \
                patch('logger._getAppCmptNames') as mockedGetAppCmptNames:
            mockedArgParsePkg.ArgumentParser.return_value = mockedParser
            mockedParser.parse_args.return_value = expectedResult
            mockedGetAppCmptNames.return_value = self.appCmpts
            testResult = dut._parseArguments()
            mockedParser.parse_args.assert_called_once()
            self.assertEqual(testResult, expectedResult, '_parseArguments '
                             'failed to return the parsed arguments.')

    def test_setInDebugModeNoDebug(self) -> None:
        """
        The _setInDebugMode function must not update the logging settings
        when the list of debug logger is empty.
        """
        expectedResult = deepcopy(_loggingSettings)
        loggersList = [self.testArg.app]
        for loggers in loggersList:
            dut._setInDebugMode(loggers)
        self.assertEqual(_loggingSettings, expectedResult, '_setInDebugMode '
                         'failed to not update the settings.')

    def test_setInDebugModeDebug(self) -> None:
        """
        The _setInDebugMode must update the logging settings of the received
        logger list.
        """
        expectedResult = deepcopy(_loggingSettings)
        expectedResult['handlers']['console']['level'] = 'DEBUG'
        expectedResult['loggers']['app.windows.main']['level'] = 'DEBUG'
        expectedResult['loggers']['app.windows.ctrlr']['level'] = 'DEBUG'
        self.testArg.app = 'app.windows.main,app.windows.ctrlr'
        loggersList = [self.testArg.app]
        for loggers in loggersList:
            dut._setInDebugMode(loggers)
        self.assertEqual(_loggingSettings, expectedResult, '_updateSettings '
                         'failed to update the settings.')

    def test_updateSettings(self) -> None:
        """
        The _updateSettings function must set in debug mode the loggers
        passed in the arguments.
        """
        expectedCalls = [call(self.testArg.app)]
        with patch.object(dut, '_setInDebugMode') as mockedSetInDebugMode:
            dut._updateSettings(self.testArg)
        mockedSetInDebugMode.assert_has_calls(expectedCalls)

    def test_initLogging(self) -> None:
        """
        The initLogging function must parse the passed arguments, update
        the logging settings dictionary and initialize the logging module
        with the updated settings.
        """
        with patch.object(dut, '_parseArguments') as mockedParseArg, \
                patch.object(dut, '_updateSettings') as mockedUpdateSettings, \
                patch(self.loggingMod) as mockedLoggingMod:
            mockedParseArg.return_value = self.testArg
            dut.initLogging()
            mockedParseArg.assert_called_once()
            mockedUpdateSettings.assert_called_once_with(self.testArg)
            mockedLoggingMod.config.dictConfig. \
                assert_called_once_with(_loggingSettings)
