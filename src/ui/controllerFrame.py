import logging
import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageTk,Image

from .calibrationMsgBox import CalibrationMsgBox

class ControllerFrame(tk.LabelFrame):
    """
    The user interface controller frame.
    """
    STERRING_ICON = './resources/icons/steering-wheel.png'
    THROTTLE_BAR_LEN = 500
    BREAK_BAR_LEN = 500

    def __init__(self, parent, controllers, *args, **kwargs):
        """
        Contructor.

        Params:
            parent:         The Application main frame parent.
            controllers:    The list of controllers.
        """
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self._logger = logging.getLogger('CTRLR_FRAME')

        self._logger.debug('initializing control frame.')
        self._parent = parent
        self._root = self._parent.nametowidget(self._parent.winfo_parent())
        self._controllers = controllers

        self._logger.debug('initializing controller selection/calibration')
        self._init_ctrlr_selection()

        self._logger.debug('initializing controller feedback')
        self._init_ctrlr_feedback()

    def _init_ctrlr_selection(self):
        """
        Initializing controller selection.
        """
        self._selectedCtrl = tk.StringVar(self._parent)
        self._selectedCtrl.set(self._controllers['list'][0].get_name())
        self._ctrlSelectLabel = tk.Label(self, text='Controller:')
        self._ctrlSelectLabel.grid(row=0, column=0, padx=10, pady=10)
        ctrlNames = []
        for controller in self._controllers['list']:
            ctrlNames.append(controller.get_name())
        self._ctrlSelectMenu = tk.OptionMenu(self, self._selectedCtrl, *ctrlNames, command=self._select_ctrl)
        self._ctrlSelectMenu.grid(row=0, column=1, padx=10, pady=10)
        self._ctrlCalibButton = tk.Button(self, text='Calibrate', command=self._calibrate_ctrl)
        self._ctrlCalibButton.grid(row=0, column=2, padx=10, pady=10)

    def _init_ctrlr_feedback(self):
        """
        Initializing the controller feedback.
        """
        feedbackState = tk.DISABLED
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

        self._root.bind('<<steering-axis>>', self._update_steering)
        self._root.bind('<<throttle-axis>>', self._update_throttle)
        self._root.bind('<<break-axis>>', self._update_break)

    def _update_steering(self, event):
        """
        Update the sterring icon with new angle.

        Params:
            modifier:      The steering modifier.
        """
        self._logger.debug('updating steering state')
        axis = self._controllers['active'].get_axis_map()
        modifier = self._controllers['active'].get_axis(axis.index('steering'))
        # TODO: check orientation for unit ??
        modifier = round(modifier, 2) * -1
        rotated_img = self._steeringImg.rotate(90 * modifier)
        self._steeringTkImg = ImageTk.PhotoImage(rotated_img)
        self._steeringIcon.create_image(1, 1, anchor=tk.NW, image=self._steeringTkImg)

    def _update_throttle(self, event):
        """
        Update the throttle progressbar.

        Params:
            modifier:       The throttle modifier.
        """
        self._logger.debug('updating throttle state')
        axis = self._controllers['active'].get_axis_map()
        modifier = self._controllers['active'].get_axis(axis.index('throttle'))
        modifier = round(modifier, 3)
        self._throttleBar['value'] = modifier * self._throttleBar['maximum']

    def _update_break(self, event):
        """
        Update the break progressbar.

        Params:
            modifier:       The break modifier.
        """
        self._logger.debug('updating break state.')
        axis = self._controllers['active'].get_axis_map()
        modifier = self._controllers['active'].get_axis(axis.index('break'))
        modifier = round(modifier, 3)
        self._breakBar['value'] = modifier * self._breakBar['maximum']

    def _select_ctrl(self, selectedCtrl):
        """
        Select a controller.
        """
        self._logger.debug(f"selecting controller: {selectedCtrl}")
        for controller in self._controllers['list']:
            if selectedCtrl == controller.get_name():
                self._controllers['active'] = controller

    def _calibrate_ctrl(self):
        """
        Calibrate the selected controller.
        """
        self._logger.debug(f"calibrating controller: {self._controllers['active'].get_name()}")
        self._calibSeq = 0
        self._root.bind('<<x-button>>', self._record_calibration)
        self._calibMsgBox = CalibrationMsgBox(self._root)

    def _record_calibration(self, event):
        """
        Record calibration value.
        """
        self._logger.info('saving calibration value.')
        self._controllers['active'].calibrate(self._calibSeq)
        self._calibSeq += 1
        self._calibMsgBox.update_msg()
