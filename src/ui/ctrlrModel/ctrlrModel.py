from PySide2.QtCore import QModelIndex
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QComboBox, QGraphicsView, QProgressBar, QPushButton

from pkgs.controller import Controller


class CtrlrModel(QStandardItemModel):
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
        super(CtrlrModel, self).__init__(0, 1)
        self._logger = appLogger.getLogger('CTRL_MODEL')
        self._calibBtn, self._ctrlrSelect, self._wheelIcon, \
            self._thrtlBar, self._brkBar = widgets
        self._controllers = {'active': None, 'list': []}
        Controller.initFramework()
        self.updateCtrlrList(appLogger)

    def _listCurrentCtrlrs(self) -> tuple:
        """
        Get the list of current controller names.

        Return:
            The list of names of current controllers.
        """
        currentNames = []
        for ctrlr in self._controllers['list']:
            currentNames.append(ctrlr.getName())
        return tuple(currentNames)

    def _filterAddedCtrlrs(self, currentList: tuple, newList: tuple) -> tuple:
        """
        Filter the added controllers.

        Params:
            currentList:    The current list of controllers.
            newList:        The new list of controllers.

        Return:
            The list of controllers to add.
        """
        addedCtrlrs = filter(lambda newCtrlr: newCtrlr not in currentList,
                             newList)
        return tuple(addedCtrlrs)

    def _filterRemovedCtrlrs(self, currentList: tuple,
                             newList: tuple) -> tuple:
        """
        Filter the controllers to be removed.

        Params:
            currentList:    The current list of controllers.
            newList:        The new list of controllers.

        Return:
            The list of controllers to remove.
        """
        removedCtrls = filter(lambda oldCtrlr: oldCtrlr not in newList,
                              currentList)
        return tuple(removedCtrls)

    def _addControllers(self, availableCtrlrs: dict, addList: tuple) -> None:
        """
        Add the new controllers.

        Params:
            availableCtrlrs:    The availabble controllers.
            addList:            The list on controllers to add.
        """

    def updateCtrlrList(self, appLogger) -> None:
        """
        Update the controller list.

        Params:
            appLogger:  The application logger.
        """
        self._logger.info('updating controller list...')
        ctrlrList = Controller.listControllers()
        controllers = []
        for ctrlName in ctrlrList:
            controllers.append(Controller(appLogger,
                                          ctrlrList[ctrlName],
                                          ctrlName))
        self._controllers = {'active': controllers[0], 'list': controllers}
        self._logger.info('controller list updated')

    # def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
    #     """
    #     Get the number of row.

    #     Return:
    #         The number of row.
    #     """
    #     return len(self._controllers['list'])

    # def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
    #     """
    #     Get the number of column.

    #     Return:
    #         The number of column.
    #     """
    #     return 1

    # def data(self, index: QModelIndex, role: int = ...) -> Any:
    #     return super().data(index, role=role)
