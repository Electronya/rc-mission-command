
from PySide2.QtSvg import QGraphicsSvgItem
from PySide2.QtWidgets import QComboBox, QGraphicsView, \
    QGraphicsScene, QProgressBar, QPushButton

from ...models.joystickModel import JoystickModel


class JoystickCtrlr():
    """
    The controllers widget controller.
    """
    THRTL_STYLESHEET = 'QProgressBar::chunk {background-color: green;}'
    BRAKE_STYLESHEET = 'QProgressBar::chunk {background-color: red;}'
    WHEEL_ICON = ':/controller/icons/steering-wheel.svg'
    WHEEL_ICON_SCALE = 0.12

    def __init__(self, logger: object, calibrate: QPushButton,
                 select: QComboBox, refresh: QPushButton,
                 wheel: QGraphicsView, thrtlBar: QProgressBar,
                 brkBar: QProgressBar) -> None:
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
        self._logger = logger.getLogger('CTRLRS-CTRLR')
        self._logger.info('intializing...')
        self._calBtn = calibrate
        self._selectCombo = select
        self._refreshBtn = refresh
        self._wheelView = wheel
        self._thrtlBar = thrtlBar
        self._brakeBar = brkBar
        self._model = JoystickModel(logger)
        self._initWidgets()
        self._logger.info('intialized')

    def _initWidgets(self):
        """
        Initialize the widgets.
        """
        self._calBtn.clicked.connect(self._model.calibrateJoystick)
        self._selectCombo.setModel(self._model.model)
        self._selectCombo.currentTextChanged. \
            connect(self._model.activateJoystick)
        self._refreshBtn.clicked.connect(self._model.updateJoystickList)
        self._initWheelWidgets()
        self._thrtlBar.setValue(0)
        self._thrtlBar.setStyleSheet(self.THRTL_STYLESHEET)
        self._brakeBar.setValue(0)
        self._brakeBar.setStyleSheet(self.BRAKE_STYLESHEET)

    def _initWheelWidgets(self):
        """
        Initialize the wheel widgets
        """
        icon = QGraphicsSvgItem(self.WHEEL_ICON)
        icon.setScale(self.WHEEL_ICON_SCALE)
        scene = QGraphicsScene()
        scene.addItem(icon)
        self._wheelView.setScene(scene)
