from unittest import TestCase
from unittest.mock import Mock, patch

from PySide2.QtWidgets import QMessageBox

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
        self.QMsgBoxCls = 'pkgs.ui.windows.appWindow.qtw.QMessageBox'
        self.joystickCtrlrCls = 'pkgs.ui.windows.appWindow.JoystickCtrlr'
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

    def test_initJoystickCtrlrCreate(self):
        """
        The _initJoystickCtrlr method must create the
        joystick UI controller.
        """
        with patch(self.joystickCtrlrCls) as mockedJoystickCtrlr:
            self.testAppWindow._initJoystickCtrlr(self.logger)
            mockedJoystickCtrlr. \
                assert_called_once_with(self.logger,
                                        self.testAppWindow.joystickCalBtn,
                                        self.testAppWindow.joystickSelect,
                                        self.testAppWindow.joystickWheelIcon,
                                        self.testAppWindow.joystickThrlBar,
                                        self.testAppWindow.joystickBrkBar)

    def test_initJoystickCtrlrConnect(self):
        """
        The _initJoystickCtrlr method must connect
        the error message box slot.
        """
        mockedJoystickCtrlr = Mock()
        with patch(self.joystickCtrlrCls) as mockedJoystickCtrlrCls:
            mockedJoystickCtrlrCls.return_value = mockedJoystickCtrlr
            self.testAppWindow._initJoystickCtrlr(self.logger)
            mockedJoystickCtrlr.error.connect.assert_called_once()

    def test_initJoystickCtrlrAvailable(self):
        """
        The _initJoystickCtrlr method must check if there are any
        available joystick.
        """
        mockedJoystickCtrlr = Mock()
        with patch(self.joystickCtrlrCls) as mockedJoystickCtrlrCls:
            mockedJoystickCtrlrCls.return_value = mockedJoystickCtrlr
            self.testAppWindow._initJoystickCtrlr(self.logger)
            mockedJoystickCtrlr.areJoystickAvailable.assert_called_once()

    def test_createErrorMsgBoxNewMsgBox(self):
        """
        The _createErrorMsgBox method must create the new message box.
        """
        mockedMsgBox = Mock()
        testLvl = QMessageBox.Warning
        testException = Exception('test error')
        with patch(self.QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            self.testAppWindow._createErrorMsgBox(testLvl, testException)
            mockedMsgBoxCls.assert_called_once_with(self.testAppWindow)
            mockedMsgBox.setWindowTitle.assert_called_once_with('Error!!')
            mockedMsgBox.setText.assert_called_once_with(str(testException))
            mockedMsgBox.setIcon.assert_called_once_with(testLvl)

    def test_createErrorMsgBoxCriticalQuit(self):
        """
        The _createErrorMsgBox method must connect the button clicked signal
        to the application quit slot when the level is critical.
        """
        mockedMsgBox = Mock()
        testException = Exception('test error')
        with patch(self.QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            testLvls = [mockedMsgBoxCls.Warning, mockedMsgBoxCls.Critical]
            for testLvl in testLvls:
                self.testAppWindow._createErrorMsgBox(testLvl, testException)
            mockedMsgBox.buttonClicked.connect.assert_called_once()

    def test_createErrorMsgBoxExec(self):
        """
        The _createErrorMsgBox method must execute the created message box.
        """
        mockedMsgBox = Mock()
        testLvl = QMessageBox.Warning
        testException = Exception('test error')
        with patch(self.QMsgBoxCls) as mockedMsgBoxCls:
            mockedMsgBoxCls.return_value = mockedMsgBox
            self.testAppWindow._createErrorMsgBox(testLvl, testException)
            mockedMsgBox.exec_.assert_called_once()
