from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from ui.windows import AppWindow    # noqa: E402


class TestAppWindow(TestCase):
    """
    AppWindow test cases.
    """
    def setUp(self) -> None:
        self.QMainwindow = 'ui.windows.appWindow.qtw.QMainWindow.__init__'
        self.logger = Mock()
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initModels'):
            self.testAppWindow = AppWindow(self.logger)

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

    def test_initModelsCtrlrModel(self):
        """
        The _initModels method must initialize the controller model.
        """
        with patch.object(self.testAppWindow, '_initCtrlrModel') \
                as mockedInitCtrlModel:
            self.testAppWindow._initModels(self.logger)
            mockedInitCtrlModel.assert_called_once_with(self.logger)
