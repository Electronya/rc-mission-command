import sys
import logging

import tkinter as tk
import tkinter.messagebox as msgBox
import tkinter.ttk as ttk

import pygame

from pkgs.controller import Controller
from pkgs.client import Client
from ui.baseFrame import BaseFrame
from pkgs.unit import Unit

pygame.init()
pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN,
                          pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:%(name)s:%(message)s')


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

        self._units = {'active': None, 'list': []}

        self.title('RC Mission Commander')
        self._logger = logging.getLogger('APP')
        self._logger.info('launcihing application...')

        self._logger.info('initializing mqtt client.')
        self._client = Client(self, '12345')
        self._logger.info('mqtt client initialized.')

        self._logger.info('initializing controller.')
        self._init_controllers(ctrlsNameList)
        self._logger.info('controller initialzed.')

        self._logger.info('initializing UI.')
        self.attributes('-zoomed', True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar",
                        foreground='red', background='red')
        style.configure("grn.Horizontal.TProgressbar",
                        foreground='green', background='green')

        self._baseFrame = BaseFrame(self, self._controllers, self._units)
        self._baseFrame.pack(fill=tk.BOTH, expand=True)
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
            ctrlrNameList:      The list of connected controller names.
        """
        self._controllers = {}
        controllers = []
        for ctrl_name in ctrlrNameList.keys():
            controllers.append(Controller(ctrlrNameList[ctrl_name],
                                          ctrl_name, self))
        self._controllers = {'active': controllers[0], 'list': controllers}

    def _process_pygame_events(self):
        """
        Process the pygame events.
        """
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self._logger.debug(f"processing joystick {event.instance_id} "
                                   f"axis {event.axis} with "
                                   f"value {event.value}")
                self._process_axis(event.instance_id, event.axis)
            if event.type == pygame.JOYBUTTONDOWN:
                self._logger.debug(f"processing joystick {event.instance_id} "
                                   f"button {event.button} down")
                buttons = self._controllers['list'][event.instance_id] \
                    .get_buttons_map()
                self.event_generate(f"<<{buttons[event.button]}-button>>")
            if event.type == pygame.JOYBUTTONUP:
                self._logger.debug(f"processing joystick {event.instance_id} "
                                   f"button {event.button} up")
            if event.type == pygame.JOYHATMOTION:
                self._logger.debug(f"processing joystick {event.instance_id} "
                                   f"hat {event.hat} with value {event.value}")

        self.after(Controller.CTRL_FRAME_RATE, self._process_pygame_events)

    def _process_axis(self, joystickIdx, axisIdx):
        """
        Processing axis event.

        Params:
            joystickIdx:    The joystick index.
            axisIdx:        The axis index.
        """
        self._logger.debug(f"processing controller {joystickIdx} "
                           f"axis {axisIdx}")
        if self._controllers['active'].get_idx() == joystickIdx \
                and self._controllers['active'].is_calibrated():
            ctrlrFunctions = self._controllers['active'].get_funct_map()
            axis = self._controllers['active'].get_axis_map()
            self.event_generate(f"<<{ctrlrFunctions[axis[axisIdx]]}-axis>>")
            if self._units['active']:
                modifier = self._controllers['active'].get_axis(axisIdx)
                unitFunctions = self._units['active'].get_functions()
                unitFunctions[ctrlrFunctions[axis[axisIdx]]](modifier)

    def add_unit(self, unitId):
        """
        Add a new unit.

        Params:
            unitId:             The new unit ID.
        """
        self._logger.info(f"new unit connected: {unitId}")
        self._units['list'].append(Unit(unitId, self._client))
        self.event_generate('<<update-unit>>')

    def remove_unit(self, unitId):
        """
        Remove a unit.

        Params:
            unitId:             The unit ID to remove.
        """
        self._logger.info(f"removing unit: {unitId}")
        for unit in self._units['list']:
            if unitId == unit.get_id():
                self._units['list'].remove(unit)
        self.event_generate('<<update-unit>>')


def list_connected_controllers():
    """
    List the connected controllers.
    """
    controllerNames = Controller.list_connected()
    logging.debug(f"controller list: {controllerNames}")
    if len(controllerNames):
        return controllerNames

    msgBox.showerror('No controller connected!!', 'Please connect a supported '
                     'controller before restarting the application.')


if __name__ == '__main__':
    connectedCtrlrs = list_connected_controllers()
    app = App(connectedCtrlrs)
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
