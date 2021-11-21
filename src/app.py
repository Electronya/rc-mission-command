import sys

from PyQt5.QtWidgets import QApplication
import pygame

from logger import initLogger
from pkgs.controller import Controller
import pkgs.mqttClient as client

from ui import AppWindow

# App constants
_CLIENT_ID = 'commander'
_CLIENT_PASSWD = '12345'
_CTRL_FRAME_RATE = 10

# App data
_globalLogger: object = None
_logger: object = None
_ui: object = None
_units = {'active': None, 'list': []}


# App customs exceptions
class NoAvailableCtrlr(Exception):
    """
    The no available controller exception.
    """
    def __init__(self) -> None:
        super().__init__('No controller available.')


# App initialization
def _initLogger() -> None:
    """
    Initialize the application logger.
    """
    global _globalLogger
    global _logger
    _globalLogger = initLogger()
    _logger = _globalLogger.getLogger('APP')
    _logger.info('launcihing application...')


def _initUserIface():
    """
    Initialize the user interface.
    """
    global _globalLogger
    global _logger
    global _ui
    _logger.info('initializing user interface...')
    _ui = AppWindow(_globalLogger)
    _logger.info('user interface initialized')


def _initPygame():
    """
    Intialize Pygame.
    """
    global _logger
    _logger.info('initializing pygame...')
    pygame.init()
    pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN,
                             pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
    _logger.info('pygame initialized')


def _initMqttClient(appLogger):
    """
    Intialize the MQTT client.

    Params:
        appLogger:  The application logger.
    """
    global _logger
    _logger.info('initializing mqtt client...')
    client.init(appLogger, _CLIENT_ID, _CLIENT_PASSWD)
    # client.registerMsgCallback(UnitCxnStateMsg.TOPIC_ROOT,
    #                            _onCxnStateMsg)
    client.startLoop()
    _logger.info('mqtt client initialized')


def _listControllers() -> dict:
    """
    List the available controllers.

    Return:
        The list of available controllers.
    """
    global _logger
    controllers = Controller.listControllers()
    _logger.debug(f"available controllers: {controllers}")
    if len(controllers) == 0:
        raise NoAvailableCtrlr()
    return controllers


def _initControllers(appLogger: object) -> None:
    """
    Initialize the controllers.

    Params:
        appLogger:  The application logger.
    """
    global _logger
    global _controllers
    _logger.info('initializing controller...')
    ctrlrList = _listControllers()
    controllers = []
    for ctrl_name in ctrlrList.keys():
        controllers.append(Controller(appLogger,
                                      ctrlrList[ctrl_name],
                                      ctrl_name))
    _controllers = {'active': controllers[0], 'list': controllers}
    _logger.info('controller initialzed')


def _init():
    """
    Initialize the Application.
    """
    global _globalLogger
    _initLogger()
    _initUserIface()
    _initPygame()
    # _initMqttClient(_globalLogger)
    # _initControllers(_globalLogger)
    # TODO: set QTimer for controller events


def quit():
    """
    Quit the application.
    """
    _logger.info('quitting the application')
    for controller in _controllers['list']:
        controller.quit()
    pygame.quit()
    client.disconnect()
    sys.exit(0)


# class App(tk.Tk):
#     """
#     The application base class.
#     """


#     def __init__(self):
#         """
#         Constructor.
#         """
#         global appLogger
#         tk.Tk.__init__(self)
#         self._units = {'active': None, 'list': []}
#         appLogger = self._initLogger()
#         self._initPygame()
#         self._initMqttClient(appLogger)
#         self._initControllers(appLogger)
#         self._initUsrInterface()
#         self.after(self.CTRL_FRAME_RATE, self._processCtrlrEvents)

#     def _setUsrInterfaceStyle(self):
#         """
#         Set the user interface style.
#         """
#         style = ttk.Style()
#         style.theme_use('clam')
#         style.configure('red.Horizontal.TProgressbar',
#                         foreground='red', background='red')
#         style.configure('grn.Horizontal.TProgressbar',
#                         foreground='green', background='green')

#     def _initUsrInterface(self) -> None:
#         """
#         Initialize the user interface.
#         """
#         self._logger.info('initializing UI...')
#         self.title('RC Mission Commander')
#         self.attributes('-zoomed', True)
#         self._setUsrInterfaceStyle()
#         self._baseFrame = BaseFrame(self, self._controllers, self._units)
#         self._baseFrame.pack(fill=tk.BOTH, expand=True)
#         self._logger.info('UI initialized')
#         self._logger.info('application launched')

#     def _processCtrlrEvents(self):
#         """
#         Process the pygame events.
#         """
#         self._controllers['active'].processEvents()
#         self.after(self.CTRL_FRAME_RATE, self._processCtrlrEvents)

#     def _addUnit(self, unitId):
#         """
#         Add a newly connected unit in the list.

#         Params:
#             unitId:     The ID of the unit to add.
#         """
#         global appLogger
#         alreadyExist = False
#         for unit in self._units['list']:
#             if unitId == unit.get_id():
#                 self._logger.warn(f"unit {unitId} already exist in the list")
#                 alreadyExist = True
#         if not alreadyExist:
#             self._logger.debug(f"adding new unit {unitId}")
#             self._units['list'].append(Unit(appLogger, client, unitId))

#     def _removeUnit(self, unitId):
#         """
#         Remove the disconnected unit.

#         Params:
#             unitId:     The ID of the unit to remove.
#         """
#         unitToRemove = [unit for unit in self._units['list']
#                         if unitId == unit.get_id()]
#         if len(unitToRemove) == 1:
#             self._logger.debug(f"removing unit {unitId}")
#             self._units['list'].remove(unitToRemove[0])
#             if unitId == self._units['active'].get_id():
#                 self._logger.debug(f"deactivating unit {unitId}")
#                 self._units['active'] = None
#         else:
#             self._logger.warn(f"{len(unitToRemove)} instance of unit "
#                               f"{unitId} found")

#     def _onCxnStateMsg(self, mqttClient, usrData, msg):
#         """
#         On connection state message callback.

#         Params:
#             mqttClient:     The MQTT client instance.
#             usrData:    The user data.
#             mgs:        The received message.
#         """
#         global appLogger
#         cxnStateMsg = UnitCxnStateMsg(self.CLIENT_ID)
#         cxnStateMsg.fromJson(msg)
#         if cxnStateMsg.isOnline():
#             self._logger.info(f"new unit connected: {cxnStateMsg.getUnit()}")
#             self._addUnit(cxnStateMsg.getUnit())
#         elif cxnStateMsg.isOffline():
#             self._logger.info(f"removing unit: {cxnStateMsg.getUnit()}")
#             self._removeUnit(cxnStateMsg.getUnit())
#         self.event_generate('<<update-unit>>')


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        _init()
        app.exec_()
    except Exception as e:
        app._logger.error(e)
