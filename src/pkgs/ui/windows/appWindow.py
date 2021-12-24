import PySide2.QtWidgets as qtw

from .appWindow_auto import Ui_MainWindow
from ..controllers.ctrlrsCtrlr import CtrlrsCtrlr


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
        self._initCtrlrs(appLogger)

    def _initCtrlrs(self, logger: object) -> None:
        """
        Initialize the UI models.

        Params:
            logger:     The application logger.
        """
        self._initCtrlrsCtrlr(logger)

    def _initCtrlrsCtrlr(self, logger: object) -> None:
        """
        Initialize the controllers controller.
        """
        self._ctrlrsCtrlr = CtrlrsCtrlr(logger, self.ctrlrCalBtn,
                                        self.ctrlrSelect, self.ctrlRefreshBtn,
                                        self.ctrlrWheelIcon, self.ctrlrThrlBar,
                                        self.ctrlrBrkBar)
