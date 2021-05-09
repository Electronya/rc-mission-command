import sys
import logging

import tkinter as tk
import tkinter.ttk as ttk

from controller import Controller
from client import Client
from ui import ControlFrame

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
        logging.basicConfig(level=logging.DEBUG)
        logging.info('launcihing application...')

        logging.info('initializing mqtt client.')
        self._client = Client('12345')
        logging.info('mqtt client initialized.')

        logging.info('initializing controller.')
        controllers = Controller.list_connected()
        logging.debug(f"controller list: {controllers}")
        self._controllers = []
        callbacks = [
            {
                'steering': self._update_steering,
                'throttle': self._update_throttle,
                'break': self._update_break,
            },
        ]
        for idx in range(len(controllers)):
            self._controllers.append(Controller(idx, controllers[idx], callbacks[idx]))
        self._activeCtrl = self._controllers[0]
        logging.info('controller initialzed.')

        logging.info('initializong UI.')
        self.attributes('-zoomed', True)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("red.Horizontal.TProgressbar", foreground='red')
        callbacks = {
            'selectCtrl': self._activate_ctrl,
            'calibrateCtrl': self._calibrate_ctrl,
        }
        self._controlFrame = ControlFrame(self, [controllers[0]], callbacks, text="Controls")
        self._controlFrame.grid(row=0, column=0, padx=10, pady=10)

        logging.info('application launched.')

    def process_ctrl_event(self):
        """
        Process the controllers events.
        """
        for controller in self._controllers:
            controller.process_events()

        self.after(self.CTRL_FRAME_RATE, self.process_ctrl_event)

    def quit(self):
        """
        Quit the application.
        """
        logging.info('quitting the application')
        self._client.disconnect()
        self.destroy()
        sys.exit()

    def _activate_ctrl(self, ctrl_name):
        """
        Activate a controller.

        Params:
            ctrl_name:      The controller name to activate.
        """
        logging.info(f"activating controller: {ctrl_name}")
        for controller in self._controllers:
            if ctrl_name == controller.get_name():
                self._activeCtrl = controller

    def _calibrate_ctrl(self):
        """
        Calibrate the active controller.
        """
        logging.info(f"calibrating controller: {self._activeCtrl.get_name()}")

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
    app.after(app.CTRL_FRAME_RATE * 100, app.process_ctrl_event)
    app.mainloop()
