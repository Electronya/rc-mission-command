from PySide2.QtWidgets import QComboBox, QGraphicsView, \
    QProgressBar, QPushButton

from ...models.ctrlrModel import CtrlrModel


class CtrlrsCtrlr():
    """
    The controllers widget controller.
    """
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
        self._wheelIcon = wheel
        self._thrtlBar = thrtlBar
        self._brkBar = brkBar
        self._model = CtrlrModel(logger)
        self._initWidgets()
        self._logger.info('intialized')

    def _initWidgets(self):
        """
        Initialize the widgets.
        """
        self._calBtn.clicked.connect(self._model.calibrateCtrlr)
        self._selectCombo.setModel(self._model.model)
        self._selectCombo.currentTextChanged.connect(self._model.activateCtrlr)
        self._refreshBtn.clicked.connect(self._model.updateCtrlrList)
