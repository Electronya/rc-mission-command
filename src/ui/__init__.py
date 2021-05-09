import logging
import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageTk,Image

class ControlFrame(tk.LabelFrame):
    """
    The user interface control frame.
    """
    STERRING_ICON = './resources/icons/steering-wheel.png'
    THROTTLE_BAR_LEN = 500
    BREAK_BAR_LEN = 500

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
        self._steeringImg = Image.open(self.STERRING_ICON)
        self._steeringTkImg = ImageTk.PhotoImage(self._steeringImg)
        self._steeringIcon = tk.Canvas(self, width=100, height=100)
        self._steeringIcon.grid(row=1, column=0, rowspan=2, padx=10, pady=10)
        self._steeringIcon.create_image(1, 1, anchor=tk.NW, image=self._steeringTkImg)
        self._throttleBar = ttk.Progressbar(self, style='grn.Horizontal.TProgressbar',
            orient=tk.HORIZONTAL, mode='determinate', length=self.THROTTLE_BAR_LEN)
        self._throttleBar.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self._breakBar = ttk.Progressbar(self, style='red.Horizontal.TProgressbar',
            orient=tk.HORIZONTAL, mode='determinate', length=self.BREAK_BAR_LEN)
        self._breakBar.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    def get_updaters(self):
        """
        Get the updater functions.

        Return:
            A dictionary contraining the updater fucntions.
        """
        return {
            "steering": self._update_steering,
            "throttle": self._update_throttle,
            "break": self._update_break,
        }

    def _update_steering(self, modifier):
        """
        Update the sterring icon with new angle.

        Params:
            modifier:      The steering modifier.
        """
        self._logger.debug('updating steering state')
        # TODO: check orientation for unit ??
        modifier = round(modifier, 2) * -1
        rotated_img = self._steeringImg.rotate(90 * modifier)
        self._steeringTkImg = ImageTk.PhotoImage(rotated_img)
        self._steeringIcon.create_image(1, 1, anchor=tk.NW, image=self._steeringTkImg)

    def _update_throttle(self, modifier):
        """
        Update the throttle progressbar.

        Params:
            modifier:       The throttle modifier.
        """
        self._logger.debug('updating throttle state')
        modifier = round(modifier, 3)
        self._throttleBar['value'] = modifier * self.THROTTLE_BAR_LEN

    def _update_break(self, modifier):
        """
        Update the break progressbar.

        Params:
            modifier:       The break modifier.
        """
        self._logger.debug('updating break state.')
        modifier = round(modifier, 3)
        self._breakBar['value'] = modifier * self.BREAK_BAR_LEN

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
