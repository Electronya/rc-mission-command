import PySide2.QtWidgets as qtw

from .appWindow_auto import Ui_MainWindow
from ..controllers.joystickCtrlr import JoystickCtrlr


class AppWindow(qtw.QMainWindow, Ui_MainWindow):
    """
    The application main window.
    """
    def __init__(self, appLogger: object) -> None:     # noqa: E501
        """
        Constructor.

        Params:
            appLoger:   The application logger.
        """
        super(AppWindow, self).__init__()
        self._logger = appLogger.getLogger('APP_WINDOW')
        self._logger.debug('loading UI...')
        self.setupUi(self)
        self._initUI(appLogger)

    def _initUI(self, logger: object) -> None:
        """
        Initialize the UI models.

        Params:
            logger:     The application logger.
        """
        self._initJoystickCtrlr(logger)

    def _initJoystickCtrlr(self, logger: object) -> None:
        """
        Initialize the joystick controller.
        """
        self._joystickCtrlr = JoystickCtrlr(logger, self.joystickCalBtn,
                                            self.joystickSelect,
                                            self.joystickWheelIcon,
                                            self.joystickThrlBar,
                                            self.joystickBrkBar)
