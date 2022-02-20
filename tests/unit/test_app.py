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
    def test_appMainInitLogger(self):
        """
        The application main function must initialize the logger.
        """
        with patch('app.initLogger') as mockedInitLogger, \
                patch('app.client'), patch('app.AppComposer'):
            app.main()
            mockedInitLogger.assert_called_once()

    def test_appMainInitClient(self):
        """
        The application main funcion must initialize the MQTT client.
        """
        logger = object()
        with patch('app.initLogger') as mockedInitLogger, \
                patch('app.client') as mockedClient, \
                patch('app.AppComposer'):
            mockedInitLogger.return_value = logger
            app.main()
            mockedClient.init.assert_called_once_with(logger,
                                                      app._CLIENT_ID,
                                                      app._CLIENT_PASSWD)

    def test_appMainAppComposer(self):
        """
        The application main function must instaciated th AppComposer
        and run it.
        """
        logger = object()
        with patch('app.initLogger') as mockedInitLogger, \
                patch('app.client'), \
                patch('app.AppComposer') as mockedAppComp:
            mockedInitLogger.return_value = logger
            app.main()
            mockedAppComp.assert_called_once_with(logger)
            mockedAppComp().run.assert_called_once()
