from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.controllers.commCtrlr import CommCtrlr     # noqa: E402


class TestCommCtrlr(TestCase):
    """
    The CommCtrlr class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.client = 'pkgs.ui.controllers.commCtrlr.commCtrlr.client'
        self.messageBox = 'pkgs.ui.controllers.commCtrlr.commCtrlr.QMessageBox'
        self.regExp = 'pkgs.ui.controllers.commCtrlr.commCtrlr.QRegExp'
        self.regExpValidatior = 'pkgs.ui.controllers.commCtrlr.commCtrlr.QRegExpValidator'  # noqa: E501
        self.mockedLogger = Mock()
        self.mockedBrokerEntry = Mock()
        self.mockedPortEntry = Mock()
        self.mockedConnectBtn = Mock()
        with patch.object(CommCtrlr, '_setupBrokerValidation'):
            self.commCtrlr = CommCtrlr(self.mockedLogger,
                                       self.mockedBrokerEntry,
                                       self.mockedPortEntry,
                                       self.mockedConnectBtn)

    def test_constructorConnectBtn(self):
        """
        The constructor must connect the connect button
        to its slot.
        """
        with patch.object(CommCtrlr, '_setupBrokerValidation'):
            CommCtrlr(self.mockedLogger, self.mockedBrokerEntry,
                      self.mockedPortEntry, self.mockedConnectBtn)
            self.mockedConnectBtn.clicked.connect \
                .assert_called()

    def test_constructorSetupBrokerValidation(self):
        """
        The constructor must setup the broker validation.
        """
        with patch.object(CommCtrlr, '_setupBrokerValidation') as mockedValid:
            CommCtrlr(self.mockedLogger, self.mockedBrokerEntry,
                      self.mockedPortEntry, self.mockedConnectBtn)
            mockedValid.assert_called_once()

    def test_setupBrokerValidation(self):
        """
        The _setupBrokerValidation method must set the broker IP
        validator.
        """
        mockedRegExp = Mock()
        mockedRegExpValid = Mock()
        with patch(self.regExpValidatior) as mockedRegExpValidConst, \
                patch(self.regExp) as mockedRegExpConst:
            mockedRegExpConst.return_value = mockedRegExp
            mockedRegExpValidConst.return_value = mockedRegExpValid
            self.commCtrlr._setupBrokerValidation()
            mockedRegExpConst \
                .assert_called_once_with(self.commCtrlr._IP_LIVE_REGEX)
            mockedRegExpValidConst \
                .assert_called_once_with(mockedRegExp, self.mockedBrokerEntry)
            self.mockedBrokerEntry.setValidator \
                .assert_called_once_with(mockedRegExpValid)

    def test_createBadBrokerMsgBox(self):
        """
        The _createBadBrokerMsgBox method must create
        the warning message box.
        """
        mockedMsgBox = Mock()
        with patch(self.messageBox) as mockedMsgBoxConst:
            mockedMsgBoxConst.return_value = mockedMsgBox
            self.commCtrlr._createBadBrokerMsgBox()
            mockedMsgBoxConst.assert_called_once()
            mockedMsgBox.setWindowTitle.assert_called_once()
            mockedMsgBox.setText.assert_called_once()
            mockedMsgBox.setIcon.assert_called_once()
            mockedMsgBox.exec_.assert_called_once()

    def test_connectButtonCallbackBadBroker(self):
        """
        The _connectButtonCallback method must validate
        broker IP address and create the warning
        message box if not valid.
        """
        self.commCtrlr._isConnected = False
        testBrokerIp = '192.168.1.1'
        self.mockedBrokerEntry.text.return_value = testBrokerIp
        mockedRegExp = Mock()
        mockedRegExp.exactMatch.return_value = False
        with patch(self.regExp) as mockedRegExpConst, \
                patch.object(self.commCtrlr, '_createBadBrokerMsgBox') \
                as mockedCreateMsgBox:
            mockedRegExpConst.return_value = mockedRegExp
            self.commCtrlr._connectButtonCallback()
            mockedRegExpConst \
                .assert_called_once_with(self.commCtrlr._IP_FINAL_REGEX)
            mockedRegExp.exactMatch.assert_called_once_with(testBrokerIp)
            mockedCreateMsgBox.assert_called_once()

    def test_connectButtonCallbackConnectError(self):
        """
        The _connectButtonCallback method must emit
        the error signal if the connection fails.
        """
        self.commCtrlr._isConnected = False
        testBrokerIp = '192.168.1.1'
        self.mockedBrokerEntry.text.return_value = testBrokerIp
        testPort = 1883
        self.mockedPortEntry.value.return_value = testPort
        mockedRegExp = Mock()
        mockedRegExp.exactMatch.return_value = True
        with patch(self.regExp) as mockedRegExpConst, \
                patch(self.client) as mockedClient, \
                patch.object(self.commCtrlr, 'error') as mockedErr:
            mockedClient.connect.side_effect = Exception('test')
            mockedRegExpConst.return_value = mockedRegExp
            self.commCtrlr._connectButtonCallback()
            mockedClient.connect.assert_called_once_with(testBrokerIp,
                                                         testPort)
            mockedErr.emit.assert_called_once_with('test')

    def test_connectButtonCallbackConnect(self):
        """
        The _connectButtonCallback method must connect to the broker.
        """
        self.commCtrlr._isConnected = False
        testBrokerIp = '192.168.1.1'
        self.mockedBrokerEntry.text.return_value = testBrokerIp
        testPort = 1883
        self.mockedPortEntry.value.return_value = testPort
        mockedRegExp = Mock()
        mockedRegExp.exactMatch.return_value = True
        with patch(self.regExp) as mockedRegExpConst, \
                patch(self.client) as mockedClient, \
                patch.object(self.commCtrlr, 'error') as mockedErr:
            mockedRegExpConst.return_value = mockedRegExp
            self.commCtrlr._connectButtonCallback()
            mockedClient.connect.assert_called_once_with(testBrokerIp,
                                                         testPort)
            mockedErr.emit.assert_not_called()

    def test_connectButtonCallbackDisconnectError(self):
        """
        The _connectButtonCallback method must emit
        the error signal if the disconnect fails.
        """
        self.commCtrlr._isConnected = True
        with patch(self.client) as mockedClient, \
                patch.object(self.commCtrlr, 'error') as mockedErr:
            mockedClient.disconnect.side_effect = Exception('test')
            self.commCtrlr._connectButtonCallback()
            mockedClient.disconnect.assert_called_once()
            mockedErr.emit.assert_called_once_with('test')

    def test_connectButtonCallbackDisconnect(self):
        """
        The _connectButtonCallback method must disconnect to the broker.
        """
        self.commCtrlr._isConnected = True
        with patch(self.client) as mockedClient, \
                patch.object(self.commCtrlr, 'error') as mockedErr:
            self.commCtrlr._connectButtonCallback()
            mockedClient.disconnect.assert_called_once()
            mockedErr.emit.assert_not_called()
