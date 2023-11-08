import logging

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QTransform
from PySide2.QtSvg import QGraphicsSvgItem
from PySide2.QtWidgets import QComboBox, QGraphicsView, \
    QGraphicsScene, QMessageBox, QProgressBar, QPushButton

from ...models.joystickModel import JoystickModel


class JoystickCtrlr(QObject):
    """
    The controllers widget controller.
    """
    THRTL_STYLESHEET = 'QProgressBar::chunk {background-color: green;}'
    BRAKE_STYLESHEET = 'QProgressBar::chunk {background-color: red;}'
    WHEEL_ICON = ':/controller/icons/steering-wheel.svg'
    WHEEL_ICON_SCALE = 0.12
    WHEEL_RANGE = 90

    error = Signal(QMessageBox.Icon, Exception)

    def __init__(self, calibrate: QPushButton, select: QComboBox,
                 wheel: QGraphicsView, thrtlBar: QProgressBar,
                 brkBar: QProgressBar) -> None:
        """
        Constructor.

        Params:
            calibrate:  The calibration button.
            select:     The controller selection combobox.
            refresh:    The refresh controller list button.
            wheel:      The wheel position icon.
            thrtlBar:   The throttle position bar.
            brkBar:     The brake position bar.
        """
        QObject.__init__(self)
        self._logger = logging.getLogger('app.windows.ctrlr')
        self._logger.info('initializing...')
        self._calBtn = calibrate
        self._selectCombo = select
        self._wheelView = wheel
        self._thrtlBar = thrtlBar
        self._brakeBar = brkBar
        self._model = JoystickModel()
        self._model.calibration.connect(self._createCalibMsgBox)
        self._model.axisMotion.connect(self._axisMotionCallback)
        self._initWidgets()
        self._logger.info('initialized')

    def _initWidgets(self) -> None:
        """
        Initialize the widgets.
        """
        self._calBtn.clicked.connect(self._model.calibrateJoystick)
        self._selectCombo.setModel(self._model.model)
        self._selectCombo.currentTextChanged \
            .connect(self._switchJoystick)
        self._initWheelWidgets()
        self._thrtlBar.setValue(0)
        self._thrtlBar.setStyleSheet(self.THRTL_STYLESHEET)
        self._brakeBar.setValue(0)
        self._brakeBar.setStyleSheet(self.BRAKE_STYLESHEET)

    def _initWheelWidgets(self) -> None:
        """
        Initialize the wheel widgets
        """
        icon = QGraphicsSvgItem(self.WHEEL_ICON)
        icon.setScale(self.WHEEL_ICON_SCALE)
        scene = QGraphicsScene()
        scene.addItem(icon)
        self._wheelView.setScene(scene)

    @Slot(str)
    def _createCalibMsgBox(self, msg: str) -> None:
        """
        Create the calibration message box.
        """
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Calibrating the joystick')
        msgBox.setText(msg)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.exec_()
        if 'done' in msg:
            self._calBtn.setEnabled(False)
        else:
            self._model.calibrateJoystick()

    @Slot(str)
    def _switchJoystick(self, joystickName: str) -> None:
        """
        Switch between connected joystick.
        """
        self._model.activateJoystick(joystickName)
        self._calBtn.setEnabled(not self._model.isJoystickCalibrated())

    def _updateSteering(self, modifier: float) -> None:
        """
        Update the steering wheel widget.

        Params:
            modifier:   The steering modifier.
        """
        transform = QTransform()
        transform.rotate(self.WHEEL_RANGE * modifier)
        self._wheelView.setTransform(transform)

    def _updateThrottle(self, modifier: float) -> None:
        """
        Update the throttle widget.

        Params:
            modifier:   The throttle modifier.
        """
        minimum = self._thrtlBar.minimum()
        thrtlRange = self._thrtlBar.maximum() - minimum
        self._thrtlBar.setValue(int((thrtlRange * modifier) + minimum))

    def _updateBrake(self, modifier: float) -> None:
        """
        Update the brake widget.

        Params:
            modifier:   The brake modifier.
        """
        minimum = self._brakeBar.minimum()
        brakeRange = self._brakeBar.maximum() - minimum
        self._brakeBar.setValue(int((brakeRange * modifier) + minimum))

    @Slot(str, int, float)
    def _axisMotionCallback(self, type: str,
                            idx: int, modifier: float) -> None:
        """
        Callback for axis motion.

        Params:
            type:       The joystick type.
            idx:        The axis index.
            modifier:   The axis modifier.
        """
        updateSwitch = (
            self._updateSteering,
            self._updateThrottle,
            self._updateBrake
        )
        updateSwitch[idx](modifier)

    def areJoystickAvailable(self) -> None:
        """
        Check if there is an available joystick.
        """
        availableCount = self._model.model.rowCount()
        if availableCount == 0:
            self._logger.error(f"available joystick count: {availableCount}")
            self.error.emit(QMessageBox.Critical,
                            Exception('No joystick are available.'))
        else:
            self._calBtn.setEnabled(not self._model.isJoystickCalibrated())
