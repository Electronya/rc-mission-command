from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from ui.ctrlrModel import CtrlrModel        # noqa: E402


class TestCtrlrModel(TestCase):
    """
    CtrlrModel test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.ctrlr = 'ui.ctrlrModel.ctrlrModel.Controller'
        self.testLogger = Mock()
        with patch.object(CtrlrModel, '_initControllers'):
            self.ctrlrMdl = CtrlrModel(self.testLogger,
                                       (None, None, None, None, None))
        self.testCtrlrList = {'test controller 1': 0, 'test controller 2': 1,
                              'test controller 3': 2, 'test controller 4': 3}

    def test_constructorInitCtrlrs(self):
        """
        The constructor must initialize the controllers.
        """
        with patch.object(CtrlrModel, '_initControllers') as mockedInitCtrlrs:
            ctrlrMdl = CtrlrModel(self.testLogger,      # noqa: F841
                                  (None, None, None, None, None))
            mockedInitCtrlrs.assert_called_once()

    def test_initCtrlrsInitFmk(self):
        """
        The initControllers method must inititialize the controllers framework.
        """
        with patch(self.ctrlr) as mockedCtrlr, \
                patch.object(mockedCtrlr, 'initFramework') as mockedInitFmk, \
                patch.object(mockedCtrlr, 'listControllers') \
                as mockedListCtrlrs:
            mockedListCtrlrs.return_value = self.testCtrlrList
            self.ctrlrMdl._initControllers(self.testLogger)
            mockedInitFmk.assert_called_once()

    def test_initCtrlrsListCtrlrs(self):
        """
        The initControllers method must list the available controllers.
        """
        with patch(self.ctrlr) as mockedCtrlr, \
                patch.object(mockedCtrlr, 'initFramework'), \
                patch.object(mockedCtrlr, 'listControllers') \
                as mockedListCtrlrs:
            mockedListCtrlrs.return_value = self.testCtrlrList
            self.ctrlrMdl._initControllers(self.testLogger)
            mockedListCtrlrs.assert_called_once()

    def test_initCtrlrsCreateCtrlrs(self):
        """
        The initControllers method must instanciate a Controller for each
        available controllers.
        """
        expectedCalls = []
        for ctrlrName in self.testCtrlrList:
            expectedCalls.append(call(self.testLogger,
                                      self.testCtrlrList[ctrlrName],
                                      ctrlrName))
        with patch(self.ctrlr) as mockedCtrlr, \
                patch.object(mockedCtrlr, 'initFramework'), \
                patch.object(mockedCtrlr, 'listControllers') \
                as mockedListCtrlrs:
            mockedListCtrlrs.return_value = self.testCtrlrList
            self.ctrlrMdl._initControllers(self.testLogger)
            mockedCtrlr.assert_has_calls(expectedCalls)
