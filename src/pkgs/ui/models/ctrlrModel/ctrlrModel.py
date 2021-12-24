from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QStandardItem, QStandardItemModel

from pkgs.controller import Controller


class CtrlrModel(QObject):
    """
    Controller model.
    """
    def __init__(self, appLogger: object) -> None:
        """
        Constructor.

        Params:
            appLogger:      The application logger.
        """
        QObject.__init__(self)
        self._appLogger = appLogger
        self._logger = appLogger.getLogger('CTRL_MODEL')
        self._logger.info('initializing...')
        self._controllers = {'active': None, 'list': []}
        self.model = QStandardItemModel(0, 1)
        Controller.initFramework()
        self.updateCtrlrList()
        self._logger.info('initialized')

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

    def _updateModel(self) -> None:
        """
        Update the controller combobox model.
        """
        self.model.clear()
        for ctrlr in self._controllers['list']:
            item = QStandardItem(ctrlr.getName())
            self.model.appendRow(item)

    def updateCtrlrList(self) -> None:
        """
        Update the controller list.
        """
        self._logger.info('updating controller list...')
        connectedCtrlrs = Controller.listControllers()
        addedCtrls = self._filterAddedCtrlrs(tuple(connectedCtrlrs))
        self._addControllers(connectedCtrlrs, addedCtrls)
        removedCtrlrs = self._filterRemovedCtrlrs(tuple(connectedCtrlrs))
        self._removeControllers(removedCtrlrs)
        self._updateModel()
        self._logger.info('controller list updated')
