import PyQt5.QtWidgets as qtw
from PyQt5 import uic


class AppWindow(qtw.QMainWindow):
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
        uic.loadUi('./src/ui/appWindow.ui', self)
        self._logger.debug('UI loaded')
        self.show()
