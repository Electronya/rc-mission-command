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
                patch.object(AppWindow, '_initUI'):
            self.testAppWindow = AppWindow(self.logger)
        self._setUpMockedWidgets()

    def _setUpMockedWidgets(self):
        """
        Setup the mocked widgets.
        """
        self.testAppWindow.joystickCalBtn = Mock()
        self.testAppWindow.joystickSelect = Mock()
        self.testAppWindow.joystickWheelIcon = Mock()
        self.testAppWindow.joystickThrlBar = Mock()
        self.testAppWindow.joystickBrkBar = Mock()

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi') as mockedSetupUi, \
                patch.object(AppWindow, '_initUI'):
            testAppWindow = AppWindow(self.logger)
            mockedSetupUi.assert_called_once_with(testAppWindow)

    def test_constructorInitUI(self) -> None:
        """
        The constructor must initialize the UI submodules.
        """
        with patch(self.QMainwindow), \
                patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUI') as mockedInitUI:
            AppWindow(self.logger)
            mockedInitUI.assert_called_once_with(self.logger)

    def test_initUiJoystickCtrlr(self):
        """
        The _initUI method must initialize the joysticks controller.
        """
        with patch.object(self.testAppWindow, '_initJoystickCtrlr') \
                as mockedInitJoystickCtrlr:
            self.testAppWindow._initUI(self.logger)
            mockedInitJoystickCtrlr. \
                assert_called_once_with(self.logger)
