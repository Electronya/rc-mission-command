import logging
import tkinter as tk

from .controllerFrame import ControllerFrame
from .unitFrame import UnitFrame


class BaseFrame(tk.Frame):
    """
    The base frame of the UI.
    """
    def __init__(self, parent, controllers, units, *args, **kwargs):
        """
        Constructor.

        Params:
            parent:             The parent of the frame.
            controllers:        The connected controllers.
            units:              The connected units.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._logger = logging.getLogger('BASE_FRM')
        self._parent = parent
        self._ctrlrList = controllers
        self._units = units

        self._logger.debug('building the controller frame')
        self._ctrlrFrame = ControllerFrame(self, self._ctrlrList,
                                           text='Controller',
                                           width=700, height=250)
        self._ctrlrFrame.grid_propagate(0)
        self._ctrlrFrame.grid(row=0, column=0, padx=10, pady=10)

        self._logger.debug('building the unit frame')
        self._unitFrame = UnitFrame(self, self._units, text='Units',
                                    width=700, height=1750)
        self._unitFrame.grid_propagate(0)
        self._unitFrame.grid(row=1, column=0, padx=10, pady=10)
