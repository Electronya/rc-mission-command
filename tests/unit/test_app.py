from unittest import TestCase
from unittest.mock import patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

import app  # noqa: E402


class TestApp(TestCase):
    """
    The app module test cases.
    """
    def test_appMainInitLogging(self):
        """
        The application main function must initialize the logging module.
        """
        with patch('app.initLogging') as mockedInitLogging, \
                patch('app.AppComposer'):
            app.main()
            mockedInitLogging.assert_called_once()

    def test_appMainAppComposer(self):
        """
        The application main function must instantiated th AppComposer
        and run it.
        """
        with patch('app.initLogging'), patch('app.AppComposer') \
                as mockedAppComp:
            app.main()
            mockedAppComp.assert_called_once_with()
            mockedAppComp().run.assert_called_once()
