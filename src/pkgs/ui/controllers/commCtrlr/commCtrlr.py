from PySide2.QtCore import QObject, QRegExp, Signal, Slot
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QLineEdit, QMessageBox, QPushButton, QSpinBox

from .... import mqttClient as client


class CommCtrlr(QObject):
    """
    The communication controller.
    """
    _IP_LIVE_REGEX = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'    # noqa: E501
    _IP_FINAL_REGEX = '^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$'

    error = Signal(str)

    def __init__(self, logger: object, brokerEntry: QLineEdit,
                 portEntry: QSpinBox, clientEntry: QLineEdit,
                 passwordEntry: QLineEdit, connectBtn: QPushButton) -> None:
        """
        The constructor.

        Params:
            logger:         The application logger.
            brokerEntry:    The entry for the broker IP.
            portEntry:      The entry for the MQTT port.
            clientEntry:    The entry for the MQTT client ID.
            passwordEntry:  The entry for the MQTT password.
            connectBtn:     The connect button.
        """
        QObject.__init__(self)
        self._logger = logger.getLogger('COMM-CTRLR')
        self._logger.info('initializing...')
        self._brokerEntry = brokerEntry
        self._setupBrokerValidation()
        self._portEntry = portEntry
        self._clientEntry = clientEntry
        self._pwdEntry = passwordEntry
        self._connectBtn = connectBtn
        self._connectBtn.clicked.connect(self._connectButtonCallback)
        self._isConnected = False
        self._logger.info('initialized')

    def _setupBrokerValidation(self) -> None:
        """
        Setup the broker entry validation.
        """
        regExp = QRegExp(self._IP_LIVE_REGEX)
        validator = QRegExpValidator(regExp, self._brokerEntry)
        self._brokerEntry.setValidator(validator)

    def _createBadBrokerMsgBox(self):
        """
        Create the bad broker IP message box.
        """
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Warning')
        msgBox.setText('Bad broker IP address.')
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.exec_()

    @Slot()
    def _connectButtonCallback(self) -> None:
        """
        The connect button callback.
        """
        brokerIp = self._brokerEntry.text()
        port = self._portEntry.value()
        if not self._isConnected:
            regExp = QRegExp(self._IP_FINAL_REGEX)
            if not regExp.exactMatch(brokerIp):
                self._logger.error('Unable to connect to the broker: Bad IP.')
                self._createBadBrokerMsgBox()
                return
            try:
                self._logger.info(f"connecting to broker {brokerIp}:{port}")
                client.connect(brokerIp, port)
            except Exception as e:
                self._logger.info(e)
                self.error.emit(str(e))
        else:
            try:
                self._logger.info(f"disconnecting from broker "
                                  f"{brokerIp}:{port}")
                client.disconnect()
            except Exception as e:
                self._logger.info(e)
                self.error.emit(str(e))
