from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.models.joystickModel import JoystickModel     # noqa: E402


class TestJoystickModel(TestCase):
    """
    JoystickModel test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.joystickCls = 'pkgs.ui.models.joystickModel.joystickModel.Joystick'                # noqa: E501
        self.QStdItem = 'pkgs.ui.models.joystickModel.joystickModel.QStandardItem'              # noqa: E501
        self.QStdItemModel = 'pkgs.ui.models.joystickModel.joystickModel.QStandardItemModel'    # noqa: E501
        self.loggingMod = 'pkgs.ui.models.joystickModel.joystickModel.logging'
        self.mockedLogger = Mock()
        self.testJoystickList = {'test controller 1': 0,
                                 'test controller 2': 1,
                                 'test controller 3': 2,
                                 'test controller 4': 3}
        self.mockedJoysticks = \
            self._setUpMockedJoysticks(self.testJoystickList)
        self.mockedStdItemModel = Mock()
        with patch(self.loggingMod) as mockedLoggingMod, \
                patch(self.joystickCls) as mockedJoystick, \
                patch.object(mockedJoystick, 'initFramework'), \
                patch.object(JoystickModel, 'updateJoystickList'), \
                patch.object(JoystickModel, 'activateJoystick'):
            mockedLoggingMod.getLogger.return_value = self.mockedLogger
            self.joystickMdl = JoystickModel()
            self.joystickMdl._joysticks['active'] = self.mockedJoysticks[0]
            self.joystickMdl._joysticks['list'] = self.mockedJoysticks
            self.joystickMdl.model = self.mockedStdItemModel

    def _setUpMockedJoysticks(self, joystickList: dict):
        """
        Setup the mocked joysticks.

        Params:
            joystickList:      The joystick list to mock.
        """
        mockedJoysticks = []
        for joystick in joystickList:
            mocked = Mock()
            mocked.getName.return_value = joystick
            mocked.getIdx.return_value = joystickList[joystick]
            mockedJoysticks.append(mocked)
        return mockedJoysticks

    def test_constructorGetLogger(self) -> None:
        """
        The constructor must get the logger.
        """
        with patch(self.loggingMod) as mockedLoggingMod, \
                patch(self.joystickCls) as mockedJoystick, \
                patch.object(mockedJoystick, 'initFramework'), \
                patch.object(JoystickModel, 'updateJoystickList'), \
                patch.object(JoystickModel, 'activateJoystick'):
            JoystickModel()
            mockedLoggingMod.getLogger \
                .assert_called_once_with('app.windows.ctrlr.model')

    def test_constructorInitJoysticks(self):
        """
        The constructor must initialize the joystick framework,
        create the combobox model and update the joystick list.
        """
        with patch(self.loggingMod), \
                patch(f"{self.joystickCls}.initFramework") as mockedInitFmk, \
                patch(self.QStdItemModel) as mockedQStdItemMdl, \
                patch.object(JoystickModel, 'updateJoystickList') \
                as mockedInitJoystickList:
            JoystickModel()
            mockedInitFmk.assert_called_once()
            mockedQStdItemMdl.assert_called_once_with(0, 1)
            mockedInitJoystickList.assert_called_once()

    def test_listCurrentJoysticks(self):
        """
        The _listCurrentJoysticks method must return the list of
        current joystick names.
        """
        testResult = self.joystickMdl._listCurrentJoysticks()
        self.assertEqual(testResult, tuple(self.testJoystickList.keys()))

    def test_filterAddedJoysticks(self):
        """
        The _filterAddedJoysticks method must return the list of
        newly added joysticks.
        """
        added = {'new controller 1': 6, 'new controller 2': 7}
        newList = {**self.testJoystickList, **added}
        testResult = self.joystickMdl._filterAddedJoysticks(newList)
        self.assertEqual(testResult, tuple(added.keys()))

    def test_filterRemovedJoysticks(self):
        """
        The _filterRemovedJoysticks method must return the list
        of joysticks that have been removed.
        """
        removed = ('test controller 2', 'test controller 4')
        newList = self.testJoystickList.copy()
        for joystick in removed:
            del newList[joystick]
        testResult = self.joystickMdl._filterRemovedJoysticks(newList)
        self.assertEqual(testResult, removed)

    def test_addJoysticks(self):
        """
        The _addJoysticks method must add the new joysticks.
        """
        added = {'new controller 1': 6, 'new controller 2': 7}
        newList = {**self.testJoystickList, **added}
        mockedNewJoysticks = self._setUpMockedJoysticks(added)
        with patch(self.joystickCls) as mockedJoystick:
            mockedJoystick.side_effect = mockedNewJoysticks
            self.joystickMdl._addJoysticks(newList, tuple(added))
            for mockedJoystick in mockedNewJoysticks:
                self.assertTrue(mockedJoystick in
                                self.joystickMdl._joysticks['list'])

    def test_removeJoysticks(self):
        """
        The _removeJoysticks method must reset the active joystick
        if it has been removed and remove the old joysticks.
        """
        first = 0
        last = len(self.testJoystickList) - 1
        joystickNames = list(self.testJoystickList.keys())
        old = (joystickNames[first], joystickNames[last])
        expectedList = self.joystickMdl._joysticks['list'].copy()
        expectedList.remove(self.joystickMdl._joysticks['list'][first])
        expectedList.remove(self.joystickMdl._joysticks['list'][last])
        self.joystickMdl._removeJoysticks(old)
        self.assertEqual(self.joystickMdl._joysticks['active'],
                         expectedList[0])
        self.assertEqual(self.joystickMdl._joysticks['list'], expectedList)

    def test_updateModelClear(self):
        """
        The _updateModel method must clear the model.
        """
        with patch(self.QStdItem):
            self.joystickMdl._updateModel()
            self.mockedStdItemModel.clear.assert_called_once()

    def test_updateModelItem(self):
        """
        The _updateModel method must create and add items
        for each controllers.
        """
        mockedItems = []
        itemCalls = []
        addItemCalls = []
        for joystick in self.testJoystickList:
            mockedItems.append(joystick)
            itemCalls.append(call(joystick))
            addItemCalls.append(call(joystick))
        with patch(self.QStdItem) as mockedStdItem:
            mockedStdItem.side_effect = mockedItems
            self.joystickMdl._updateModel()
            mockedStdItem.assert_has_calls(itemCalls)
            self.joystickMdl.model.appendRow.assert_has_calls(addItemCalls)

    def test_calibrateJoystick(self):
        """
        The calibrateJoystick method must call the active joystick calibrate
        method.
        """
        self.joystickMdl.calibrateJoystick()
        self.joystickMdl._joysticks['active'].calibrate.assert_called_once()

    def test_isJoystickCalibrated(self):
        """
        The isJoystickCalibrated method must return the calibration state
        of the active joystick.
        """
        expectedStates = (True, False)
        self.joystickMdl._joysticks['active'] \
            .isCalibrated.side_effect = expectedStates
        for expectedState in expectedStates:
            if expectedState:
                self.assertTrue(self.joystickMdl.isJoystickCalibrated())
            else:
                self.assertFalse(self.joystickMdl.isJoystickCalibrated())

    def test_activateJoystickDeactivate(self):
        """
        The activateJoystick methode must deactivate the
        currently active joystick.
        """
        joystickIdx = 3
        oldJoystick = self.joystickMdl._joysticks['active']
        self.joystickMdl. \
            activateJoystick(tuple(self.testJoystickList.keys())[joystickIdx])
        oldJoystick.deactivate.assert_called_once()

    def test_activateJoystickActivate(self):
        """
        The activateJoystick methode must activate the joystick with
        the given name.
        """
        joystickIdx = 3
        self.joystickMdl. \
            activateJoystick(tuple(self.testJoystickList.keys())[joystickIdx])
        self.assertEqual(self.joystickMdl._joysticks['active'],
                         self.mockedJoysticks[joystickIdx])
        self.mockedJoysticks[joystickIdx].activate.assert_called_once()

    def test_activateJoystickSignals(self):
        """
        The activateJoystick methode must connect to the newly
        active joystick signals.
        """
        joystickIdx = 3
        self.joystickMdl. \
            activateJoystick(tuple(self.testJoystickList.keys())[joystickIdx])
        self.mockedJoysticks[joystickIdx].axisMotion \
            .connect.assert_called_once
        self.mockedJoysticks[joystickIdx].buttonDown \
            .connect.assert_called_once()
        self.mockedJoysticks[joystickIdx].buttonUp \
            .connect.assert_called_once()
        self.mockedJoysticks[joystickIdx].hatMotion \
            .connect.assert_called_once()
        self.mockedJoysticks[joystickIdx].calibration \
            .connect.assert_called_once()

    def test_updateJoystickListListConnected(self):
        """
        The updateJoystickList method must list the currently
        connected joysticks.
        """
        with patch.object(self.joystickMdl, '_updateModel'), \
                patch(f"{self.joystickCls}.listAvailable") \
                as mockedListJoysticks:
            mockedListJoysticks.return_value = {}
            self.joystickMdl.updateJoystickList()
            mockedListJoysticks.assert_called_once()

    def test_updateJoystickListFilterAdd(self):
        """
        The updateJoystickList method must filter the
        newly added joysticks.
        """
        with patch.object(self.joystickMdl, '_updateModel'), \
                patch(f"{self.joystickCls}.listAvailable") \
                as mockedJoystickList, \
                patch.object(self.joystickMdl, '_filterAddedJoysticks') \
                as mockedFilterAdded:
            mockedJoystickList.return_value = self.testJoystickList
            self.joystickMdl.updateJoystickList()
            mockedFilterAdded. \
                assert_called_once_with(tuple(self.testJoystickList))

    def test_updateJoystickListAddNew(self):
        """
        The updateJoystickList method must add the new joysticks.
        """
        newJoysticks = {"new controller 1": 5, "new controller 2": 6}
        newJoystickList = {**self.testJoystickList, **newJoysticks}
        with patch.object(self.joystickMdl, '_updateModel'), \
                patch(f"{self.joystickCls}.listAvailable") \
                as mockedJoystickList, \
                patch.object(self.joystickMdl, '_addJoysticks') \
                as mockedAddJoysticks:
            mockedJoystickList.return_value = newJoystickList
            print(self.joystickMdl._joysticks['list'])
            self.joystickMdl.updateJoystickList()
            mockedAddJoysticks.assert_called_once_with(newJoystickList,
                                                       tuple(newJoysticks))

    def test_updateJoystickListFilterRemove(self):
        """
        The updateJoystickList method must filter the
        removed joysticks.
        """
        with patch.object(self.joystickMdl, '_updateModel'), \
                patch(f"{self.joystickCls}.listAvailable") \
                as mockedJoystickList, \
                patch.object(self.joystickMdl, '_filterRemovedJoysticks') \
                as mockedFilterRemove:
            mockedJoystickList.return_value = self.testJoystickList
            self.joystickMdl.updateJoystickList()
            mockedFilterRemove. \
                assert_called_once_with(tuple(self.testJoystickList))

    def test_updateJoystickListRemoveOld(self):
        """
        The updateJoystickList method must remove the old joysticks.
        """
        joysticks2Remove = ['test controller 2', 'test controller 4']
        newJoystickList = self.testJoystickList.copy()
        for joystick2Remove in joysticks2Remove:
            del newJoystickList[joystick2Remove]
        with patch.object(self.joystickMdl, '_updateModel'), \
                patch(f"{self.joystickCls}.listAvailable") \
                as mockedJoystickList, \
                patch.object(self.joystickMdl, '_removeJoysticks') \
                as mockedRemove:
            mockedJoystickList.return_value = newJoystickList
            self.joystickMdl.updateJoystickList()
            mockedRemove.assert_called_once_with(tuple(joysticks2Remove))

    def test_updateJoystickListUpdateModel(self):
        """
        The updateJoystickList method must update the selection combobox.
        """
        with patch.object(self.joystickMdl, '_updateModel') \
                as mockedUpdateModel, \
                patch(f"{self.joystickCls}.listAvailable") \
                as mockedJoystickList:
            mockedJoystickList.return_value = self.testJoystickList
            self.joystickMdl.updateJoystickList()
            mockedUpdateModel.assert_called_once()
