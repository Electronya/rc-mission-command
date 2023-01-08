import logging
import sys

import PySide2.QtCore as qtc
import PySide2.QtWidgets as qtw

from .appWindow_auto import Ui_MainWindow
from ..controllers.joystickCtrlr import JoystickCtrlr


class AppWindow(qtw.QMainWindow, Ui_MainWindow):
    """
    The application main window.
    """
    def __init__(self) -> None:
        """
        Constructor.
        """
        super(AppWindow, self).__init__()
        self._logger = logging.getLogger('app.windows.main')
        self._logger.info('loading UI...')
        self.setupUi(self)
        self._initUI()

    def _initUI(self) -> None:
        """
        Initialize the UI models.
        """
        self._initJoystickCtrlr()

    def _initJoystickCtrlr(self) -> None:
        """
        Initialize the joystick controller.
        """
        self._joystickCtrlr = JoystickCtrlr(self.joystickCalBtn,
                                            self.joystickSelect,
                                            self.joystickWheelIcon,
                                            self.joystickThrlBar,
                                            self.joystickBrkBar)
        self._joystickCtrlr.error.connect(self._createErrorMsgBox)
        self._joystickCtrlr.areJoystickAvailable()

    @qtc.Slot(qtw.QMessageBox.Icon, Exception)
    def _createErrorMsgBox(self, lvl: qtw.QMessageBox.Icon,
                           error: Exception) -> None:
        """
        Create a error message box.
        """
        self._logger.error(f"error: {str(error)}")
        msgBox = qtw.QMessageBox(self)
        msgBox.setWindowTitle('Error!!')
        msgBox.setText(str(error))
        msgBox.setIcon(lvl)
        if lvl == qtw.QMessageBox.Critical:
            self._logger.debug('connecting to button clicked for critical')
            msgBox.buttonClicked.connect(lambda i: sys.exit(1))
        msgBox.exec_()
