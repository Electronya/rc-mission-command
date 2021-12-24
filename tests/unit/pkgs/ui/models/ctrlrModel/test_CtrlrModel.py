from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models.ctrlrModel import CtrlrModel     # noqa: E402


class TestCtrlrModel(TestCase):
    """
    CtrlrModel test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.ctrlr = 'pkgs.ui.models.ctrlrModel.ctrlrModel.Controller'
        self.QStdItem = 'pkgs.ui.models.ctrlrModel.ctrlrModel.QStandardItem'
        self.QStdItemModel = 'pkgs.ui.models.ctrlrModel.ctrlrModel.QStandardItemModel'   # noqa: E501
        self.testLogger = Mock()
        self.testCtrlrList = {'test controller 1': 0, 'test controller 2': 1,
                              'test controller 3': 2, 'test controller 4': 3}
        self.mockedCtrlrs = self._setUpMockedCtrlrs(self.testCtrlrList)
        self.mockedStdItemModel = Mock()
        with patch(self.ctrlr) as mockedCtrlr, \
                patch.object(mockedCtrlr, 'initFramework'), \
                patch.object(CtrlrModel, 'updateCtrlrList'):
            self.ctrlrMdl = CtrlrModel(self.testLogger)
            self.ctrlrMdl._controllers['active'] = self.mockedCtrlrs[0]
            self.ctrlrMdl._controllers['list'] = self.mockedCtrlrs
            self.ctrlrMdl.model = self.mockedStdItemModel

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

    def test_constructorInitCtrlrs(self):
        """
        The constructor must initialize the controller framework,
        create the combobox model and update the controller list.
        """
        with patch(f"{self.ctrlr}.initFramework") as mockedinitFmk, \
                patch(self.QStdItemModel) as mockedQStdItemMdl, \
                patch.object(CtrlrModel, 'updateCtrlrList') \
                as mockedInitCtrlrs:
            CtrlrModel(self.testLogger)
            mockedinitFmk.assert_called_once()
            mockedQStdItemMdl.assert_called_once_with(0, 1)
            mockedInitCtrlrs.assert_called_once()

    def test_listCurrentCtrlrs(self):
        """
        The _listCurrentCtrlrs method must return the list of
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
        testResult = self.ctrlrMdl._filterAddedCtrlrs(newList)
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
        testResult = self.ctrlrMdl._filterRemovedCtrlrs(newList)
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

    def test_removeControllers(self):
        """
        The _removeControllers method must reset the active controller
        if it has been removed and remove the old controllers.
        """
        first = 0
        last = len(self.testCtrlrList) - 1
        ctrlrNames = list(self.testCtrlrList.keys())
        oldCtrlrs = (ctrlrNames[first], ctrlrNames[last])
        expectedCtrlrList = self.ctrlrMdl._controllers['list'].copy()
        expectedCtrlrList.remove(self.ctrlrMdl._controllers['list'][first])
        expectedCtrlrList.remove(self.ctrlrMdl._controllers['list'][last])
        self.ctrlrMdl._removeControllers(oldCtrlrs)
        self.assertEqual(self.ctrlrMdl._controllers['active'], None)
        self.assertEqual(self.ctrlrMdl._controllers['list'], expectedCtrlrList)

    def test_updateModelClear(self):
        """
        The _updateModel method must clear the model.
        """
        with patch(self.QStdItem):
            self.ctrlrMdl._updateModel()
            self.mockedStdItemModel.clear.assert_called_once()

    def test_updateModelItem(self):
        """
        The _updateModel method must create and add items
        for each controllers.
        """
        mockedItems = []
        itemCalls = []
        addItemCalls = []
        for ctrlr in self.testCtrlrList:
            mockedItems.append(ctrlr)
            itemCalls.append(call(ctrlr))
            addItemCalls.append(call(ctrlr))
        with patch(self.QStdItem) as mockedStdItem:
            mockedStdItem.side_effect = mockedItems
            self.ctrlrMdl._updateModel()
            mockedStdItem.assert_has_calls(itemCalls)
            self.ctrlrMdl.model.appendRow.assert_has_calls(addItemCalls)

    def test_updateCtrlrListListConnected(self):
        """
        The updateCtrlrList method must list the currently
        connected controllers.
        """
        with patch.object(self.ctrlrMdl, '_updateModel'), \
                patch(f"{self.ctrlr}.listControllers") \
                as mockedListCtrlrs:
            mockedListCtrlrs.return_value = {}
            self.ctrlrMdl.updateCtrlrList()
            mockedListCtrlrs.assert_called_once()

    def test_updateCtrlrListFilterAdd(self):
        """
        The updateCtrlrList method must filter the
        newly added controllers.
        """
        with patch.object(self.ctrlrMdl, '_updateModel'), \
                patch(f"{self.ctrlr}.listControllers") as mockedCtrlList, \
                patch.object(self.ctrlrMdl, '_filterAddedCtrlrs') \
                as mockedFilterAdded:
            mockedCtrlList.return_value = self.testCtrlrList
            self.ctrlrMdl.updateCtrlrList()
            mockedFilterAdded. \
                assert_called_once_with(tuple(self.testCtrlrList))

    def test_updateCtrlrListAddNew(self):
        """
        The updateCtrlrList method must add the new controllers.
        """
        newCtrlrs = {"new controller 1": 5, "new controller 2": 6}
        newCtrlrList = {**self.testCtrlrList, **newCtrlrs}
        with patch.object(self.ctrlrMdl, '_updateModel'), \
                patch(f"{self.ctrlr}.listControllers") as mockedCtrlList, \
                patch.object(self.ctrlrMdl, '_addControllers') \
                as mockedAddCtrlrs:
            mockedCtrlList.return_value = newCtrlrList
            print(self.ctrlrMdl._controllers['list'])
            self.ctrlrMdl.updateCtrlrList()
            mockedAddCtrlrs.assert_called_once_with(newCtrlrList,
                                                    tuple(newCtrlrs))

    def test_updateCtrlrListFilterRemove(self):
        """
        The updateCtrlrList method must filter the
        removed controllers.
        """
        with patch.object(self.ctrlrMdl, '_updateModel'), \
                patch(f"{self.ctrlr}.listControllers") as mockedCtrlrList, \
                patch.object(self.ctrlrMdl, '_filterRemovedCtrlrs') \
                as mockedFilterRemove:
            mockedCtrlrList.return_value = self.testCtrlrList
            self.ctrlrMdl.updateCtrlrList()
            mockedFilterRemove. \
                assert_called_once_with(tuple(self.testCtrlrList))

    def test_updateCtrlrListRemoveOld(self):
        """
        The updateCtrlrList method must remove the old controllers.
        """
        ctrlrs2Remove = ['test controller 2', 'test controller 4']
        newCtrlrList = self.testCtrlrList.copy()
        for ctrlr2Remove in ctrlrs2Remove:
            del newCtrlrList[ctrlr2Remove]
        with patch.object(self.ctrlrMdl, '_updateModel'), \
                patch(f"{self.ctrlr}.listControllers") as mockedCtrlrList, \
                patch.object(self.ctrlrMdl, '_removeControllers') \
                as mockedRemoveCtrlr:
            mockedCtrlrList.return_value = newCtrlrList
            self.ctrlrMdl.updateCtrlrList()
            mockedRemoveCtrlr.assert_called_once_with(tuple(ctrlrs2Remove))

    def test_updateCtrlrListUpdateModel(self):
        """
        The updateCtrlrList method must update the selection combobox.
        """
        with patch.object(self.ctrlrMdl, '_updateModel') \
                as mockedUpdateModel, \
                patch(f"{self.ctrlr}.listControllers") as mockedCtrlrList:
            mockedCtrlrList.return_value = self.testCtrlrList
            self.ctrlrMdl.updateCtrlrList()
            mockedUpdateModel.assert_called_once()
