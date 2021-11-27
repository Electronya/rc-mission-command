from PyQt5.QtWidgets import QComboBox, QGraphicsView, QProgressBar, QPushButton

from pkgs.controller import Controller


class CtrlrModel():
    """
    Controller model.
    """
    def __init__(self, appLogger: object, widgets: tuple) -> None:
        """
        Constructor.

        Params:
            appLogger:  The application logger.
            widgets:    The wigeds controlled by the model
        """
        super(CtrlrModel, self).__init__()
        self._logger = appLogger.getLogger('CTRL_MODEL')
        self._calibBtn, self._ctrlrSelect, self._wheelIcon, \
            self._thrtlBar, self._brkBar = widgets
        self._initControllers(appLogger)

    def _initControllers(self, appLogger) -> None:
        """
        Initialize the controllers.

        Params:
            appLogger:  The application logger.
        """
        self._logger.info('initializing controllers...')
        Controller.initFramework()
        ctrlrList = Controller.listControllers()
        controllers = []
        for ctrlName in ctrlrList:
            controllers.append(Controller(appLogger,
                                          ctrlrList[ctrlName],
                                          ctrlName))
        self._controllers = {'active': controllers[0], 'list': controllers}
        self._logger.info('controllers initialized')
