import sys
import logging

import tkinter as tk
import tkinter.messagebox as msgBox
import tkinter.ttk as ttk

import pygame

from controller import Controller
from client import Client
from ui.baseFrame import BaseFrame

pygame.init()
pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

class App(tk.Tk):
    """
    The application base class.
    """
    CTRL_FRAME_RATE = 10

    def __init__(self, ctrlsNameList):
        """
        Constructor.

        Params:
            ctrlrNameList       The list of connected controller names.
        """
        tk.Tk.__init__(self)
        self.title('RC Mission Commander')
        self._logger = logging.getLogger('APP')
        self._logger.info('launcihing application...')

        self._logger.info('initializing mqtt client.')
        self._client = Client('12345')
        self._logger.info('mqtt client initialized.')

        self._logger.info('initializing controller.')
        self._init_controllers(ctrlsNameList)
        self._logger.info('controller initialzed.')

        self._logger.info('initializing UI.')
        self.attributes('-zoomed', True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        style.configure("grn.Horizontal.TProgressbar", foreground='green', background='green')

        self._baseFrame = BaseFrame(self, self._controllers)
        self._baseFrame.pack(fill=tk.BOTH, expand=True)
        self._uiUpdaters = self._baseFrame.get_updaters()
        self._logger.info('UI initialized.')

        self.after(Controller.CTRL_FRAME_RATE, self._process_pygame_events)

        self._logger.info('application launched.')

    def quit(self):
        """
        Quit the application.
        """
        self._logger.info('quitting the application')
        for controller in self._controllers['list']:
            controller.quit()
        pygame.quit()
        self._client.disconnect()
        self.destroy()
        sys.exit()

    def _init_controllers(self, ctrlrNameList):
        """
        Initialize the controllers.

        Params:
            ctrlrNameList       The list of connected controller names.
        """
        self._controllers = {}
        controllers = []
        for ctrl_name in ctrlrNameList.keys():
            controllers.append(Controller(ctrlrNameList[ctrl_name], ctrl_name, self))
        self._controllers = {'active': controllers[0], 'list': controllers}

    def _process_pygame_events(self):
        """
        Process the pygame events.
        """
        self._logger.debug('processing events')
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self._logger.debug(f"processing joystick {event.instance_id} axis {event.axis} with value {event.value}")
                functions = self._controllers['list'][event.instance_id].get_funct_map()
                axis = self._controllers['list'][event.instance_id].get_axis_map()
                self._uiUpdaters['controller'][functions[axis[event.axis]]](event.value)
            if event.type == pygame.JOYBUTTONDOWN:
                self._logger.debug(f"processing joystick {event.instance_id} button {event.button} down")
            if event.type == pygame.JOYBUTTONUP:
                self._logger.debug(f"processing joystick {event.instance_id} button {event.button} up")
            if event.type == pygame.JOYHATMOTION:
                self._logger.debug(f"processing joystick {event.instance_id} hat {event.hat} with value {event.value}")

        self.after(Controller.CTRL_FRAME_RATE, self._process_pygame_events)

def list_connected_controllers():
    """
    List the connected controllers.
    """
    controllerNames = Controller.list_connected()
    logging.debug(f"controller list: {controllerNames}")
    if len(controllerNames):
        return controllerNames

    msgBox.showerror('No controller connected!!', 'Please connect a supported controller before restarting the application.')

if __name__ == '__main__':
    connectedCtrlrs = list_connected_controllers()
    app = App(connectedCtrlrs)
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
