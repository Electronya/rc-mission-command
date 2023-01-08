import logging
import sys

from PySide2.QtWidgets import QApplication

from .windows import AppWindow


class AppComposer:
    """
    Application Composer.
    """
    def __init__(self) -> None:
        """
        Constructor.
        """
        self._logger = logging.getLogger('app.composer')
        self._logger.info('creating Qt app')
        self._app = QApplication(sys.argv)
        self._logger.debug('creating UI')
        self._appWindow = AppWindow()

    def run(self):
        """
        Run the application.
        """
        self._appWindow.show()
        sys.exit(self._app.exec_())
