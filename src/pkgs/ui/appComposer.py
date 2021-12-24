import sys

from PySide2.QtWidgets import QApplication

from .windows import AppWindow


class AppComposer:
    """
    Application Composer.
    """
    def __init__(self, logger: object) -> None:
        """
        Constructor.
        """
        self._logger = logger.getLogger('APP_COMP')
        self._logger.info('creating Qt app')
        self._app = QApplication(sys.argv)
        self._logger.debug('creating UI')
        self._appWindow = AppWindow(logger)

    def run(self):
        """
        Run the application.
        """
        self._appWindow.show()
        sys.exit(self._app.exec_())
