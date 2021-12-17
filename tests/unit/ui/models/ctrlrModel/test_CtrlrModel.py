from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from ui.models.ctrlrModel import CtrlrModel     # noqa: E402


class TestCtrlrModel(TestCase):
    """
    CtrlrModel test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.ctrlr = 'ui.models.ctrlrModel.ctrlrModel.Controller'
        self.testLogger = Mock()
        self.testCtrlrList = {'test controller 1': 0, 'test controller 2': 1,
                              'test controller 3': 2, 'test controller 4': 3}
        self._setUpMockedWidgets()
        with patch(self.ctrlr) as mockedCtrlr, \
                patch.object(mockedCtrlr, 'initFramework'), \
                patch.object(mockedCtrlr, 'listControllers') \
                as mockedListCtrlrs:
            mockedCtrlr.side_effect = \
                self._setUpMockedCtrlrs(self.testCtrlrList)
            mockedListCtrlrs.return_value = self.testCtrlrList
            self.ctrlrMdl = CtrlrModel(self.testLogger, self.calBtn,
                                       self.ctrlrSelect, self.refreshBtn,
                                       self.wheelIcon, self.thrtlBar,
                                       self.brkBar)

    def _setUpMockedCtrlrs(self, ctrlrList: dict):
        """
        Setup the mocked controllers.

        Params:
            ctrlrList:      The controller list to mock.
        """
        mockedCtrlrs = []
        for testCtrlr in ctrlrList:
            mockedCtrlr = Mock()
            mockedCtrlr.getName.return_value = testCtrlr
            mockedCtrlr.getIdx.return_value = ctrlrList[testCtrlr]
            mockedCtrlrs.append(mockedCtrlr)
        return mockedCtrlrs

    def _setUpMockedWidgets(self):
        """
        Setup the mocked widgets.
        """
        self.calBtn = Mock(),
        self.ctrlrSelect = Mock()
        self.refreshBtn = Mock()
        self.wheelIcon = Mock()
        self.thrtlBar = Mock()
        self.brkBar = Mock()

    def test_constructorInitCtrlrs(self):
        """
        The constructor must initialize the controller framework
        and update the controller list.
        """
        with patch(f"{self.ctrlr}.initFramework") as mockedinitFmk, \
                patch.object(CtrlrModel, '_updateCtrlrList') \
                as mockedInitCtrlrs:
            CtrlrModel(self.testLogger, None, None, None, None, None, None)
            mockedinitFmk.assert_called_once()
            mockedInitCtrlrs.assert_called_once()

    def test_listCurrentCtrlrs(self):
        """
        The _listCurrentCtrlrs mehod must return the list of
        current controller names.
        """
        testResult = self.ctrlrMdl._listCurrentCtrlrs()
        self.assertEqual(testResult, tuple(self.testCtrlrList.keys()))

    def test_filterAddedCtrlrs(self):
        """
        The _filterAddedCtrlrs method must return the list of
        newly added controllers.
        """
        addedCtrlrs = {'new controller 1': 6, 'new controller 2': 7}
        newList = {**self.testCtrlrList, **addedCtrlrs}
        testResult = self.ctrlrMdl._filterAddedCtrlrs(tuple(self.testCtrlrList),    # noqa: E501
                                                      newList)
        self.assertEqual(testResult, tuple(addedCtrlrs.keys()))

    def test_filterRemovedCtrlrs(self):
        """
        The _filterRemovedCtrlrs method must return the list
        of controllers that have been removed.
        """
        removedCtrlrs = ('test controller 2', 'test controller 4')
        newList = self.testCtrlrList.copy()
        for ctrlr in removedCtrlrs:
            del newList[ctrlr]
        testResult = self.ctrlrMdl._filterRemovedCtrlrs(tuple(self.testCtrlrList),  # noqa: E501
                                                        newList)
        self.assertEqual(testResult, removedCtrlrs)

    def test_addControllers(self):
        """
        The _addControllers method must add the new controllers.
        """
        addedCtrlrs = {'new controller 1': 6, 'new controller 2': 7}
        newList = {**self.testCtrlrList, **addedCtrlrs}
        mockedNewCtrlrs = self._setUpMockedCtrlrs(addedCtrlrs)
        with patch(self.ctrlr) as mockedCtrlr:
            mockedCtrlr.side_effect = mockedNewCtrlrs
            self.ctrlrMdl._addControllers(newList, tuple(addedCtrlrs))
            for mockedCtrlr in mockedNewCtrlrs:
                self.assertTrue(mockedCtrlr in
                                self.ctrlrMdl._controllers['list'])

    def test_initCtrlrsListCtrlrs(self):
        """
        The initControllers method must list the available controllers.
        """
        with patch(self.ctrlr) as mockedCtrlr, \
                patch.object(mockedCtrlr, 'initFramework'), \
                patch.object(mockedCtrlr, 'listControllers') \
                as mockedListCtrlrs:
            mockedListCtrlrs.return_value = self.testCtrlrList
            self.ctrlrMdl._updateCtrlrList(self.testLogger)
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
            self.ctrlrMdl._updateCtrlrList(self.testLogger)
            mockedCtrlr.assert_has_calls(expectedCalls)
