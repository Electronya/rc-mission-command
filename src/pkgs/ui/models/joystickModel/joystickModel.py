from os import name
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QStandardItem, QStandardItemModel

from pkgs.joystick import Joystick


class JoystickModel(QObject):
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
        self._joysticks = {'active': None, 'list': []}
        self.model = QStandardItemModel(0, 1)
        Joystick.initFramework()
        self.updateJoystickList()
        self._logger.info('initialized')

    def _listCurrentJoysticks(self) -> tuple:
        """
        Get the list of current joystick names.

        Return:
            The list of names of current joysticks.
        """
        currentNames = []
        for joystick in self._joysticks['list']:
            currentNames.append(joystick.getName())
        return tuple(currentNames)

    def _filterAddedJoysticks(self, newList: tuple) -> tuple:
        """
        Filter the added joysticks.

        Params:
            newList:        The new list of joysticks.

        Return:
            The list of joysticks to add.
        """
        currentList = map(lambda joystick: joystick.getName(),
                          self._joysticks['list'])
        added = filter(lambda joystick: joystick not in currentList,
                       newList)
        return tuple(added)

    def _filterRemovedJoysticks(self, newList: tuple) -> tuple:
        """
        Filter the joysticks to be removed.

        Params:
            newList:        The new list of joysticks.

        Return:
            The list of joysticks to remove.
        """
        currentList = map(lambda joystick: joystick.getName(),
                          self._joysticks['list'])
        removed = filter(lambda joystick: joystick not in newList,
                         currentList)
        return tuple(removed)

    def _addJoysticks(self, availables: dict, addList: tuple) -> None:
        """
        Add the new joysticks.

        Params:
            availables:         The available joysticks.
            addList:            The list of joysticks to add.
        """
        for joystick in addList:
            self._joysticks['list'].append(Joystick(self._appLogger,
                                                    availables[joystick],
                                                    joystick))

    def _removeJoysticks(self, removeList: tuple) -> None:
        """
        Removed the old joysticks.

        Params:
            removeList:         The list of joysticks to remove.
        """
        for joystick in self._joysticks['list']:
            if joystick.getName() in removeList:
                self._joysticks['list'].remove(joystick)
        if self._joysticks['active'] and \
                self._joysticks['active'].getName() in removeList:
            self._joysticks['active'] = self._joysticks['list'][0]

    def _updateModel(self) -> None:
        """
        Update the controller combobox model.
        """
        self.model.clear()
        for joystick in self._joysticks['list']:
            item = QStandardItem(joystick.getName())
            self.model.appendRow(item)

    def calibrateJoystick(self) -> None:
        """
        Calibrate the active joystick.
        TODO: Setup the calibraton.
        """
        self._logger.info(f"calibrating joystick "
                          f"{self._joysticks['active'].getName()}")

    def activateJoystick(self, joystickName: str) -> None:
        """
        Activate joystick.

        Params:
            joystickName:   The name of the joystick to activate.
        """
        self._logger.info(f"activating joystick {joystickName}")
        active = tuple(filter(lambda joystick: joystickName == joystick.getName(),  # noqa: E501
                              self._joysticks['list']))
        self._logger.debug(active)
        self._joysticks['active'] = active[0]

    def updateJoystickList(self) -> None:
        """
        Update the joystick list.
        """
        self._logger.info('updating joystick list...')
        connected = Joystick.listAvailable()
        self._logger.debug(connected)
        added = self._filterAddedJoysticks(tuple(connected))
        self._logger.debug(added)
        self._addJoysticks(connected, added)
        removed = self._filterRemovedJoysticks(tuple(connected))
        self._logger.debug(removed)
        self._removeJoysticks(removed)
        self._updateModel()
        self._logger.info('controller list updated')
