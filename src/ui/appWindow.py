import PySide2.QtWidgets as qtw
import PySide2.QtCore as qtc
from PySide2.QtUiTools import QUiLoader


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
        uiFile = qtc.QFile('./src/ui/appWindow.ui')
        uiFile.open(qtc.QFile.ReadOnly)
        loader = QUiLoader()
        uic.loadUi('./src/ui/appWindow.ui', self)
        self._logger.debug('UI loaded')
        self.show()
