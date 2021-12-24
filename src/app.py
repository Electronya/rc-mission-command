import pygame

from logger import initLogger
from pkgs.controller import Controller
import pkgs.mqttClient as client

from pkgs.ui import AppComposer

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
# class NoAvailableCtrlr(Exception):
#     """
#     The no available controller exception.
#     """
#     def __init__(self) -> None:
#         super().__init__('No controller available.')


# # App initialization
# def _initLogger() -> None:
#     """
#     Initialize the application logger.
#     """
#     global _globalLogger
#     global _logger
#     _globalLogger = initLogger()
#     _logger = _globalLogger.getLogger('APP')
#     _logger.info('launcihing application...')


# def _initPygame():
#     """
#     Intialize Pygame.
#     """
#     global _logger
#     _logger.info('initializing pygame...')
#     pygame.init()
#     pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN,
#                              pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
#     _logger.info('pygame initialized')


# def _initMqttClient(appLogger):
#     """
#     Intialize the MQTT client.

#     Params:
#         appLogger:  The application logger.
#     """
#     global _logger
#     _logger.info('initializing mqtt client...')
#     client.init(appLogger, _CLIENT_ID, _CLIENT_PASSWD)
#     # client.registerMsgCallback(UnitCxnStateMsg.TOPIC_ROOT,
#     #                            _onCxnStateMsg)
#     client.startLoop()
#     _logger.info('mqtt client initialized')


# def _listControllers() -> dict:
#     """
#     List the available controllers.

#     Return:
#         The list of available controllers.
#     """
#     global _logger
#     controllers = Controller.listControllers()
#     _logger.debug(f"available controllers: {controllers}")
#     if len(controllers) == 0:
#         raise NoAvailableCtrlr()
#     return controllers


# def _initControllers(appLogger: object) -> None:
#     """
#     Initialize the controllers.

#     Params:
#         appLogger:  The application logger.
#     """
#     global _logger
#     global _controllers
#     _logger.info('initializing controller...')
#     ctrlrList = _listControllers()
#     controllers = []
#     for ctrl_name in ctrlrList.keys():
#         controllers.append(Controller(appLogger,
#                                       ctrlrList[ctrl_name],
#                                       ctrl_name))
#     _controllers = {'active': controllers[0], 'list': controllers}
#     _logger.info('controller initialzed')


# def _init():
#     """
#     Initialize the Application.
#     """
#     global _globalLogger
#     _initLogger()
#     _initPygame()
#     _initMqttClient(_globalLogger)
#     _initControllers(_globalLogger)
#     TODO: set QTimer for controller events


def main():
    """
    Application main.
    """
    logger = initLogger()
    app = AppComposer(logger)
    app.run()


if __name__ == '__main__':
    main()
