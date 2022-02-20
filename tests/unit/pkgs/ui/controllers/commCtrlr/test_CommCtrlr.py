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
        self.regExp = 'pkgs.ui.controllers.commCtrlr.commCtrlr.QRegExp'
        self.regExpValidatior = 'pkgs.ui.controllers.commCtrlr.commCtrlr.QRegExpValidator'  # noqa: E501
        self.mockedLogger = Mock()
        self.mockedBrokerEntry = Mock()
        self.mockedPortEntry = Mock()
        self.mockedClientEntry = Mock()
        self.mockedPwdEntry = Mock()
        self.mockedConnectBtn = Mock()
        with patch.object(CommCtrlr, '_setupBrokerValidation'):
            self.commCtrlr = CommCtrlr(self.mockedLogger,
                                       self.mockedBrokerEntry,
                                       self.mockedPortEntry,
                                       self.mockedClientEntry,
                                       self.mockedPwdEntry,
                                       self.mockedConnectBtn)

    def test_constructorConnectBtn(self):
        """
        The constructor must connect the connect button
        to its slot.
        """
        with patch.object(CommCtrlr, '_setupBrokerValidation'):
            CommCtrlr(self.mockedLogger, self.mockedBrokerEntry,
                      self.mockedPortEntry, self.mockedClientEntry,
                      self.mockedPwdEntry, self.mockedConnectBtn)
            self.mockedConnectBtn.clicked.connect \
                .assert_called()

    def test_constructorSetupBrokerValidation(self):
        """
        The constructor must setup the broker validation.
        """
        with patch.object(CommCtrlr, '_setupBrokerValidation') as mockedValid:
            CommCtrlr(self.mockedLogger, self.mockedBrokerEntry,
                      self.mockedPortEntry, self.mockedClientEntry,
                      self.mockedPwdEntry, self.mockedConnectBtn)
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
