import PySide2.QtWidgets as qtw

from .appWindow_auto import Ui_MainWindow
from ..models.ctrlrModel import CtrlrModel


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
        self._initModels(appLogger)

    def _initModels(self, logger: object) -> None:
        """
        Initialize the UI models.

        Params:
            logger:     The application logger.
        """
        self._initCtrlrModel(logger)

    def _initCtrlrModel(self, logger: object) -> None:
        """
        Initialize the controller model.
        """
        self._ctrlrModel = CtrlrModel(logger, self.ctrlrCalBtn,
                                      self.ctrlrSelect, self.ctrlRefreshBtn,
                                      self.ctrlrWheelIcon, self.ctrlrThrlBar,
                                      self.ctrlrBrkBar)
