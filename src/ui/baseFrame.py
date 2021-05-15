import logging
import tkinter as tk

from .controllerFrame import ControllerFrame

class BaseFrame(tk.Frame):
    """
    The base frame of the UI.
    """
    def __init__(self, parent, controllers, *args, **kwargs):
        """
        Constructor.

        Params:
            parent              The parent of the frame.
            controllers         The connected controllers.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._logger = logging.getLogger('BASE_FRM')
        self._ctrlrList = controllers

        self._logger.debug("building the controller frame")
        self._ctrlrFrame = ControllerFrame(self, self._ctrlrList, text='Controller')
        self._ctrlrFrame.grid(row=0, column=0, padx=10, pady=10)

    def get_updaters(self):
        """
        Get the UI updaters.
        """
        updaters = {'controller': self._ctrlrFrame.get_updaters()}

        return updaters
