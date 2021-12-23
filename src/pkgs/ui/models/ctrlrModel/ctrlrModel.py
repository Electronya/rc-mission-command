from PySide2.QtCore import QModelIndex
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QComboBox, QGraphicsView, \
    QProgressBar, QPushButton

from pkgs.controller import Controller


class CtrlrModel(QStandardItemModel):
    """
    Controller model.
    """
    def __init__(self, appLogger: object, calBtn: QPushButton,
                 ctrlrSelect: QComboBox, refreshBtn: QPushButton,
                 wheelIcon: QGraphicsView, thrtlBar: QProgressBar,
                 brkBar: QProgressBar) -> None:
        """
        Constructor.

        Params:
            appLogger:      The application logger.
            calBtn:         The calibration button.
            ctrlrSelect:    The controller selection combo box.
            refreshBtn:     The controller list refresh button.
            wheelIcon:      The wheel icon.
            thrtlBar:       The throttle bar.
            brkBar:         The brake bar.
        """
        super(CtrlrModel, self).__init__(0, 1)
        self._appLogger = appLogger
        self._logger = appLogger.getLogger('CTRL_MODEL')
        self._calibBtn = calBtn
        self._ctrlrSelect = ctrlrSelect
        self._refreshBtn = refreshBtn
        self._wheelIcon = wheelIcon
        self._thrtlBar = thrtlBar
        self._brkBar = brkBar
        # self._ctrlrSelect.setModel(self)
        self._controllers = {'active': None, 'list': []}
        Controller.initFramework()
        self._updateCtrlrList()

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

    def _filterAddedCtrlrs(self, newList: tuple) -> tuple:
        """
        Filter the added controllers.

        Params:
            newList:        The new list of controllers.

        Return:
            The list of controllers to add.
        """
        currentList = map(lambda ctrlr: ctrlr.getName(),
                          self._controllers['list'])
        addedCtrlrs = filter(lambda newCtrlr: newCtrlr not in currentList,
                             newList)
        return tuple(addedCtrlrs)

    def _filterRemovedCtrlrs(self, newList: tuple) -> tuple:
        """
        Filter the controllers to be removed.

        Params:
            newList:        The new list of controllers.

        Return:
            The list of controllers to remove.
        """
        currentList = map(lambda ctrlr: ctrlr.getName(),
                          self._controllers['list'])
        removedCtrls = filter(lambda oldCtrlr: oldCtrlr not in newList,
                              currentList)
        return tuple(removedCtrls)

    def _addControllers(self, availableCtrlrs: dict, addList: tuple) -> None:
        """
        Add the new controllers.

        Params:
            availableCtrlrs:    The available controllers.
            addList:            The list of controllers to add.
        """
        for ctrlr in addList:
            self._controllers['list'].append(Controller(self._appLogger,
                                                        availableCtrlrs[ctrlr],
                                                        ctrlr))

    def _removeControllers(self, removeList: tuple) -> None:
        """
        Removed the old controllers.

        Params:
            removeList:         The list of controllers to remove.
        """
        if self._controllers['active'] and \
                self._controllers['active'].getName() in removeList:
            self._controllers['active'] = None
        for ctrlr in self._controllers['list']:
            if ctrlr.getName() in removeList:
                self._controllers['list'].remove(ctrlr)

    def _updateCtrlrList(self) -> None:
        """
        Update the controller list.
        """
        self._logger.info('updating controller list...')
        connectedCtrlrs = Controller.listControllers()
        addedCtrls = self._filterAddedCtrlrs(tuple(connectedCtrlrs))
        self._addControllers(connectedCtrlrs, addedCtrls)
        removedCtrlrs = self._filterRemovedCtrlrs(tuple(connectedCtrlrs))
        self._removeControllers(removedCtrlrs)
        self._logger.info('controller list updated')

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Get the number of row.

        Return:
            The number of row.
        """
        return len(self._controllers['list'])

    # def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
    #     """
    #     Get the number of column.

    #     Return:
    #         The number of column.
    #     """
    #     return 1

    # def data(self, index: QModelIndex, role: int = ...) -> Any:
    #     return super().data(index, role=role)
