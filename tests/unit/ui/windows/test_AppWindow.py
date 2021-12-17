from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from ui.windows import AppWindow


class TestAppWindow(TestCase):
    """
    AppWindow test cases.
    """
    def setUp(self) -> None:
        self.QMainwindow = 'ui.windows.appWindow.qtw.QMainWindow.__init__'
        self.logger = Mock()

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi') as mockedSetupUi, \
                patch.object(AppWindow, '_initModels'):
            testAppWindow = AppWindow(self.logger)
            mockedSetupUi.assert_called_once_with(testAppWindow)

    def test_constructorInitModels(self) -> None:
        """
        The constructor must initialize the UI models.
        """
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initModels') as mockedInitModels:
            AppWindow(self.logger)
            mockedInitModels.assert_called_once_with(self.logger)
