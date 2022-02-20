
from PySide2.QtCore import QObject, Signal, Slot
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

    error = Signal(QMessageBox.Icon, Exception)

    def __init__(self, logger: object, calibrate: QPushButton,
                 select: QComboBox, wheel: QGraphicsView,
                 thrtlBar: QProgressBar, brkBar: QProgressBar) -> None:
        """
        Constructor.

        Params:
            logger:     The application logger.
            calibrate:  The calibration button.
            select:     The controller selection combobox.
            refresh:    The refresh controller list button.
            wheel:      The wheel position icon.
            thrtlBar:   The throttle position bar.
            brkBar:     The brake position bar.
        """
        QObject.__init__(self)
        self._logger = logger.getLogger('JOYSTICK-CTRLR')
        self._logger.info('intializing...')
        self._calBtn = calibrate
        self._selectCombo = select
        self._wheelView = wheel
        self._thrtlBar = thrtlBar
        self._brakeBar = brkBar
        self._model = JoystickModel(logger)
        self._model.calibration.connect(self.createCalibMsgBox)
        self._initWidgets()
        self._logger.info('intialized')

    def _initWidgets(self) -> None:
        """
        Initialize the widgets.
        """
        self._calBtn.clicked.connect(self._model.calibrateJoystick)
        self._selectCombo.setModel(self._model.model)
        self._selectCombo.currentTextChanged \
            .connect(self._model.activateJoystick)
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

    @Slot(str)
    def createCalibMsgBox(self, msg: str) -> None:
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
