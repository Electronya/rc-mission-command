import PySide2.QtWidgets as qtw

from .appWindow_auto import Ui_MainWindow


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
