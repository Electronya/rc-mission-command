import logging
import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageTk,Image

class ControlFrame(tk.LabelFrame):
    """
    The user interface control frame.
    """
    STERRING_ICON = './resources/icons/steering-wheel.png'

    def __init__(self, parent, controllers, callbacks, *args, **kwargs):
        """
        Contructor.

        Params:
            parent:         The Application main frame parent.
            controllers:    The controller name list.
            callbacks:      A dictionary containing the callbacks.
        """
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self._logger = logging.getLogger('CTRL_FRAME')

        self._logger.debug('initializing control frame.')
        self._parent = parent
        self._controllers = controllers
        self._callbacks = callbacks

        # Controller selection
        self._selectedCtrl = tk.StringVar(self._parent)
        self._selectedCtrl.set(self._controllers[0])
        self._ctrlSelectLabel = tk.Label(self, text='Controller:')
        self._ctrlSelectLabel.grid(row=0, column=0, padx=10, pady=10)
        self._ctrlSelectMenu = tk.OptionMenu(self, self._selectedCtrl, *self._controllers, command=self._select_ctrl)
        self._ctrlSelectMenu.grid(row=0, column=1, padx=10, pady=10)
        self._ctrlCalibButton = tk.Button(self, text='Calibrate', command=self._calibrate_ctrl)
        self._ctrlCalibButton.grid(row=0, column=2, padx=10, pady=10)

        # Controller information
        self._steeringAngle = 0
        self._steeringImg = ImageTk.PhotoImage(Image.open(self.STERRING_ICON))
        self._steeringIcon = tk.Canvas(self, width=100, height=100)
        self._steeringIcon.grid(row=1, column=0, rowspan=2, padx=10, pady=10)
        self._steeringIcon.create_image(1, 1, anchor=tk.NW, image=self._steeringImg)
        self._throttleBar = ttk.Progressbar(self, style='red.Horizontal.TProgressbar', orient=tk.HORIZONTAL, mode='determinate', length=500)
        self._throttleBar.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self._breakBar = ttk.Progressbar(self, style='red.Horizontal.TProgressbar', orient=tk.HORIZONTAL, mode='determinate', length=500)
        self._breakBar.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    def update_steering(self, modifier):
        """
        Update the sterring icon with new angle.

        Params:
            modifier:      The steering modifier.
        """
        self._steeringImg = self._steeringImg.rotate(self._steeringAngle * -1)
        self._steeringAngle = 90 * modifier
        self._steeringImg = self._steeringImg.rotate(self._steeringAngle)

    def update_throttle(self, modifier):
        """
        Update the throttle progressbar.

        Params:
            modifier:       The throttle modifier.
        """
        self._throttleBar['value'] = modifier * 100

    def update_break(self, modifier):
        """
        Uppdate the break progressbar.

        Params:
            modifier:       The break modifier.
        """
        self._breakBar['value'] = modifier * 100

    def _select_ctrl(self, selectedCtrl):
        """
        Select a controller.
        """
        self._logger.debug(f"selecting controller: {selectedCtrl}")
        self._callbacks['selectCtrl'](selectedCtrl)

    def _calibrate_ctrl(self):
        """
        Calibrate the selected controller.
        """
        self._logger.debug(f"calibrating controller: {self._selectedCtrl.get()}")
        self._callbacks['calibrateCtrl']()
