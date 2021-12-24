from unittest import TestCase
from unittest.mock import Mock, call, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.controllers.ctrlrsCtrlr import CtrlrsCtrlr     # noqa: E402


class TestCtrlrsCtrlr(TestCase):
    """
    The CtrlrsCtrlr class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.ctrlrModel = 'pkgs.ui.controllers.ctrlrsCtrlr.ctrlrsCtrlr.CtrlrModel'          # noqa: E501
        self.graphicScene = 'pkgs.ui.controllers.ctrlrsCtrlr.ctrlrsCtrlr.QGraphicsScene'    # noqa: E501
        self.graphSvgItem = 'pkgs.ui.controllers.ctrlrsCtrlr.ctrlrsCtrlr.QGraphicsSvgItem'        # noqa: E501
        self.mockedLogger = Mock()
        self.mockedCtrlrModel = Mock()
        self.mockedGraphScene = Mock()
        self.mockedGraphSvgItem = Mock()
        self._setUpMockedWidgets()
        with patch(self.ctrlrModel) as mockedCtrlrMdl, \
                patch.object(CtrlrsCtrlr, '_initWidgets'):
            mockedCtrlrMdl.return_value = self.mockedCtrlrModel
            self.ctrlrsCtrl = CtrlrsCtrlr(self.mockedLogger, self.mockedCalBtn,
                                          self.mockedCtrlrSelect,
                                          self.mockedRefreshBtn,
                                          self.mockedWheelView,
                                          self.mockedThrtlBar,
                                          self.mockedBrkBar)

    def _setUpMockedWidgets(self):
        """
        Setup the mocked widgets.
        """
        self.mockedCalBtn = Mock()
        self.mockedCtrlrSelect = Mock()
        self.mockedRefreshBtn = Mock()
        self.mockedWheelView = Mock()
        self.mockedThrtlBar = Mock()
        self.mockedBrkBar = Mock()

    def test_constructorModel(self):
        """
        The constructor must instantiate the model.
        """
        with patch(self.ctrlrModel) as mockedCtrlrMdl, \
                patch.object(CtrlrsCtrlr, '_initWidgets'):
            CtrlrsCtrlr(self.mockedLogger, self.mockedCalBtn,
                        self.mockedCtrlrSelect, self.mockedRefreshBtn,
                        self.mockedWheelView, self.mockedThrtlBar,
                        self.mockedBrkBar)
            mockedCtrlrMdl.assert_called_once_with(self.mockedLogger)

    def test_constructorInitWidgets(self):
        """
        The constructor must initialize the widgets.
        """
        with patch(self.ctrlrModel), \
                patch.object(CtrlrsCtrlr, '_initWidgets') as mockedInitWidgets:
            CtrlrsCtrlr(self.mockedLogger, self.mockedCalBtn,
                        self.mockedCtrlrSelect, self.mockedRefreshBtn,
                        self.mockedWheelView, self.mockedThrtlBar,
                        self.mockedBrkBar)
            mockedInitWidgets.assert_called_once()

    def test_initWidgetsCalBtn(self):
        """
        The _initWidgets method must connect the calibration button
        to the calibration slots and disable it.
        """
        with patch.object(self.ctrlrsCtrl, '_initWheelWidgets'):
            self.ctrlrsCtrl._initWidgets()
            self.mockedCalBtn.setEnabled.assert_called_once_with(False)
            self.mockedCalBtn.clicked.connect. \
                assert_called_once_with(self.mockedCtrlrModel.calibrateCtrlr)

    def test_initWidgetsSelect(self):
        """
        The _initWidgets method must set the combobox model and connect
        the selection change to the activate controller slot.
        """
        with patch.object(self.ctrlrsCtrl, '_initWheelWidgets'):
            self.ctrlrsCtrl._initWidgets()
            self.mockedCtrlrSelect.setModel. \
                assert_called_once_with(self.mockedCtrlrModel.model)
            self.mockedCtrlrSelect.currentTextChanged.connect. \
                assert_called_once_with(self.mockedCtrlrModel.activateCtrlr)

    def test_initWidgetsRefreshBtn(self):
        """
        The _initWidgets method must connect the refresh button
        to the update controller list slot.
        """
        with patch.object(self.ctrlrsCtrl, '_initWheelWidgets'):
            self.ctrlrsCtrl._initWidgets()
            self.mockedRefreshBtn.clicked.connect. \
                assert_called_once_with(self.mockedCtrlrModel.updateCtrlrList)

    def test_initWidgetsWheel(self):
        """
        The _initWidgets method must initialize the wheel icon widgets.
        """
        with patch.object(self.ctrlrsCtrl, '_initWheelWidgets') \
                as mockedInitWheelWidgets:
            self.ctrlrsCtrl._initWidgets()
            mockedInitWheelWidgets.assert_called_once()

    def test_initWidgetsClearAndColorBars(self):
        """
        The _initWidgets method must clear and set the color
        of the throttle and brake bars.
        """
        with patch.object(self.ctrlrsCtrl, '_initWheelWidgets'):
            self.ctrlrsCtrl._initWidgets()
            self.mockedThrtlBar.setValue.assert_called_once_with(0)
            self.mockedThrtlBar.setStyleSheet. \
                assert_called_once_with(self.ctrlrsCtrl.THRTL_STYLESHEET)
            self.mockedBrkBar.setValue.assert_called_once_with(0)
            self.mockedBrkBar.setStyleSheet. \
                assert_called_once_with(self.ctrlrsCtrl.BRAKE_STYLESHEET)

    def test_initWheelWidgetsCreateScene(self):
        """
        The _initWheelWidgets method must create the graphic scene
        and add the wheel icon to it.
        """
        with patch(self.graphicScene) as mockedGraphScene, \
                patch(self.graphSvgItem) as mockedGraphSvgItem:
            mockedGraphScene.return_value = self.mockedGraphScene
            mockedGraphSvgItem.return_value = self.mockedGraphSvgItem
            self.ctrlrsCtrl._initWheelWidgets()
            mockedGraphSvgItem. \
                assert_called_once_with(self.ctrlrsCtrl.WHEEL_ICON)
            self.mockedGraphSvgItem.setScale. \
                assert_called_once_with(self.ctrlrsCtrl.WHEEL_ICON_SCALE)
            mockedGraphScene.assert_called_once()
            self.mockedGraphScene.addItem. \
                assert_called_once_with(self.mockedGraphSvgItem)
            self.mockedWheelView.setScene. \
                assert_called_once_with(self.mockedGraphScene)
