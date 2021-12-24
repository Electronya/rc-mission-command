from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.windows import AppWindow    # noqa: E402


class TestAppWindow(TestCase):
    """
    AppWindow test cases.
    """
    def setUp(self) -> None:
        self.QMainwindow = 'pkgs.ui.windows.appWindow.qtw.QMainWindow.__init__'
        self.logger = Mock()
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initCtrlrs'):
            self.testAppWindow = AppWindow(self.logger)

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi') as mockedSetupUi, \
                patch.object(AppWindow, '_initCtrlrs'):
            testAppWindow = AppWindow(self.logger)
            mockedSetupUi.assert_called_once_with(testAppWindow)

    def test_constructorInitModels(self) -> None:
        """
        The constructor must initialize the UI models.
        """
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initCtrlrs') as mockedInitCtrlrs:
            AppWindow(self.logger)
            mockedInitCtrlrs.assert_called_once_with(self.logger)

    def test_initCtrlrsCtrlrsCtrlr(self):
        """
        The _initCtrlrs method must initialize the controllers controller.
        """
        with patch.object(self.testAppWindow, '_initCtrlrsCtrlr') \
                as mockedInitCtrlModel:
            self.testAppWindow._initCtrlrs(self.logger)
            mockedInitCtrlModel.assert_called_once_with(self.logger)
