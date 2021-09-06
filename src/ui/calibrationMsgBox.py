import logging
import tkinter as tk

class CalibrationMsgBox():
    """
    The message box class.
    """
    MESSAGES = [
        'Turn the steering wheel fully LEFT and press x.',
        'Turn the steering wheel fully RIGHT and press x.',
        'Make sure the throttle is fully DEPRESSED and press x.',
        'Make sure the throttle is fully PRESSED and press x.',
        'Make sure the break is fully DEPRESSED and press x.',
        'Make sure the break is fully PRESSED and press x.',
    ]

    def __init__(self, root, *args, **kwargs):
        """
        Contructor.

        Params:
            root:       The application root.
            msg:        The message box initial message.
            buttons:    The buttons to display.
        """
        self._msgIdx = 0
        self._logger = logging.getLogger('CALIB_MSG')

        topWidth = 1000
        topHeight = 100
        topPosX = int((root.winfo_width() / 2) - topWidth / 2)
        topPosY = int((root.winfo_height() / 2) - topHeight / 2)
        self._top = tk.Toplevel(root)
        self._top.title("Controller Calibration")
        self._top.geometry(f"{topWidth}x{topHeight}+{topPosX}+{topPosY}")
        self._top.grab_set()
        self._msg = tk.StringVar(self._top)
        self._msg.set(self.MESSAGES[self._msgIdx])
        self._msgLabel = tk.Label(self._top, textvariable=self._msg)
        self._msgLabel.place(x=500, y=50, anchor='center')

    def update_msg(self):
        """
        Update the message box message.
        """
        self._logger.debug('updating message')
        self._msgIdx += 1
        if self._msgIdx == len(self.MESSAGES):
            self._top.destroy()
        self._logger.debug(f"new msg: {self.MESSAGES[self._msgIdx]}")
        self._msg.set(self.MESSAGES[self._msgIdx])

