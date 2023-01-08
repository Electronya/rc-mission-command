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
        self.QMainWindow = 'pkgs.ui.windows.appWindow.qtw.QMainWindow.__init__'
        self.QMsgBoxCls = 'pkgs.ui.windows.appWindow.qtw.QMessageBox'
        self.joystickCtrlrCls = 'pkgs.ui.windows.appWindow.JoystickCtrlr'
        self.loggingMod = 'pkgs.ui.windows.appWindow.logging'
        self.mockedLogger = Mock()
        with patch(self.loggingMod) as mockedLoggingMod, \
                patch(self.QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUI'):
            mockedLoggingMod.getLogger.return_value = self.mockedLogger
            self.testAppWindow = AppWindow()
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

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the main window logger.
        """
        with patch(self.loggingMod) as mockedLoggingMod, \
                patch(self.QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUI'):
            AppWindow()
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.main')

    def test_constructorSetupUi(self) -> None:
        """
        The constructor must setup the UI.
        """
        with patch(self.QMainWindow), \
                patch(self.QMainWindow), \
                patch.object(AppWindow, 'setupUi') as mockedSetupUi, \
                patch.object(AppWindow, '_initUI'):
            testAppWindow = AppWindow()
            mockedSetupUi.assert_called_once_with(testAppWindow)

    def test_constructorInitUI(self) -> None:
        """
        The constructor must initialize the UI submodules.
        """
        with patch(self.QMainWindow), \
                patch(self.QMainWindow), patch.object(AppWindow, 'setupUi'), \
                patch.object(AppWindow, '_initUI') as mockedInitUI:
            AppWindow()
            mockedInitUI.assert_called_once()

    def test_initUiJoystickCtrlr(self):
        """
        The _initUI method must initialize the joysticks controller.
        """
        with patch.object(self.testAppWindow, '_initJoystickCtrlr') \
                as mockedInitJoystickCtrlr:
            self.testAppWindow._initUI()
            mockedInitJoystickCtrlr.assert_called_once()

    def test_initJoystickCtrlrCreate(self):
        """
        The _initJoystickCtrlr method must create the
        joystick UI controller.
        """
        with patch(self.joystickCtrlrCls) as mockedJoystickCtrlr:
            self.testAppWindow._initJoystickCtrlr()
            mockedJoystickCtrlr. \
                assert_called_once_with(self.testAppWindow.joystickCalBtn,
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
            self.testAppWindow._initJoystickCtrlr()
            mockedJoystickCtrlr.error.connect.assert_called_once()

    def test_initJoystickCtrlrAvailable(self):
        """
        The _initJoystickCtrlr method must check if there are any
        available joystick.
        """
        mockedJoystickCtrlr = Mock()
        with patch(self.joystickCtrlrCls) as mockedJoystickCtrlrCls:
            mockedJoystickCtrlrCls.return_value = mockedJoystickCtrlr
            self.testAppWindow._initJoystickCtrlr()
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
