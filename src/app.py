import sys
import logging

import tkinter as tk
import tkinter.ttk as ttk

import pygame

from controller import Controller
from client import Client
from ui import ControlFrame

pygame.init()
pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s:%(levelname)s:%(message)s')

class App(tk.Tk):
    """
    The application base class.
    """
    CTRL_FRAME_RATE = 10

    def __init__(self):
        """
        Constructor.
        """
        tk.Tk.__init__(self)
        self._logger = logging.getLogger('APP')
        self._logger.info('launcihing application...')

        self._logger.info('initializing mqtt client.')
        self._client = Client('12345')
        self._logger.info('mqtt client initialized.')

        self._logger.info('initializing controller.')
        controllers = Controller.list_connected()
        self._logger.debug(f"controller list: {controllers}")
        self._controllers = []
        for ctrl_name in controllers.keys():
            self._controllers.append(Controller(controllers[ctrl_name], ctrl_name, self))
        self._activeCtrl = self._controllers[0]
        self._logger.info('controller initialzed.')

        self._logger.info('initializong UI.')
        self.attributes('-zoomed', True)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar", foreground='red')
        callbacks = {
            'selectCtrl': self._activate_ctrl,
            'calibrateCtrl': self._calibrate_ctrl,
        }
        self._controlFrame = ControlFrame(self, list(controllers.keys()), callbacks, text="Controls")
        self._controlFrame.grid(row=0, column=0, padx=10, pady=10)

        self.after(Controller.CTRL_FRAME_RATE, self._process_pygame_events)

        self._logger.info('application launched.')

    def quit(self):
        """
        Quit the application.
        """
        self._logger.info('quitting the application')
        for controller in self._controllers:
            controller.quit()
        pygame.quit()
        self._client.disconnect()
        self.destroy()
        sys.exit()

    def _process_pygame_events(self):
        """
        Process the pygame events.
        """
        self._logger.debug('processing events')
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self._logger.debug(f"processing joystick {event.instance_id} axis {event.axis} with value {event.value}")
            if event.type == pygame.JOYBUTTONDOWN:
                self._logger.debug(f"processing joystick {event.instance_id} button {event.button} down")
            if event.type == pygame.JOYBUTTONUP:
                self._logger.debug(f"processing joystick {event.instance_id} button {event.button} up")
            if event.type == pygame.JOYHATMOTION:
                self._logger.debug(f"processing joystick {event.instance_id} hat {event.hat} with value {event.value}")

        self.after(Controller.CTRL_FRAME_RATE, self._process_pygame_events)

    def _activate_ctrl(self, ctrl_name):
        """
        Activate a controller.

        Params:
            ctrl_name:      The controller name to activate.
        """
        self._logger.info(f"activating controller: {ctrl_name}")
        for controller in self._controllers:
            if ctrl_name == controller.get_name():
                self._activeCtrl = controller

    def _calibrate_ctrl(self):
        """
        Calibrate the active controller.
        """
        self._logger.info(f"calibrating controller: {self._activeCtrl.get_name()}")

    def _update_steering(self, modifier):
        """
        Update the steering.

        Params:
            modifier:       The steering modifier.
        """
        self._controlFrame.update_steering(modifier)

    def _update_throttle(self, modifier):
        """
        Update the throttle.

        Params:
            modifier:       The throttle modifier.
        """
        self._controlFrame.update_throttle(modifier)

    def _update_break(self, modifier):
        """
        Update the break.

        Params:
            modifier:       The break modifier.
        """
        self._controlFrame.update_break(modifier)

if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
