from unittest import TestCase
from unittest.mock import Mock, patch

import os
import sys

sys.path.append(os.path.abspath('./src'))

from pkgs.ui.controllers.joystickCtrlr import JoystickCtrlr     # noqa: E402


class TestJoystickCtrlr(TestCase):
    """
    The JoystickCtrlr class test cases.
    """
    def setUp(self):
        """
        Test cases setup.
        """
        self.joystickModelCls = 'pkgs.ui.controllers.joystickCtrlr.joystickCtrlr.JoystickModel'     # noqa: E501
        self.qObject = 'pkgs.ui.controllers.joystickCtrlr.joystickCtrlr.QObject'                    # noqa: E501
        self.graphicScene = 'pkgs.ui.controllers.joystickCtrlr.joystickCtrlr.QGraphicsScene'        # noqa: E501
        self.graphSvgItem = 'pkgs.ui.controllers.joystickCtrlr.joystickCtrlr.QGraphicsSvgItem'      # noqa: E501
        self.mockedLogger = Mock()
        self.mockedJoystickModel = Mock()
        self.mockedGraphScene = Mock()
        self.mockedGraphSvgItem = Mock()
        self._setUpMockedWidgets()
        with patch(self.joystickModelCls) as mockedJoystickMdl, \
                patch(self.qObject), \
                patch.object(JoystickCtrlr, '_initWidgets'):
            mockedJoystickMdl.return_value = self.mockedJoystickModel
            self.joystickCtrlr = JoystickCtrlr(self.mockedLogger,
                                               self.mockedCalBtn,
                                               self.mockedJoystickSelect,
                                               self.mockedWheelView,
                                               self.mockedThrtlBar,
                                               self.mockedBrkBar)

    def _setUpMockedWidgets(self):
        """
        Setup the mocked widgets.
        """
        self.mockedCalBtn = Mock()
        self.mockedJoystickSelect = Mock()
        self.mockedRefreshBtn = Mock()
        self.mockedWheelView = Mock()
        self.mockedThrtlBar = Mock()
        self.mockedBrkBar = Mock()

    def test_constructorModel(self):
        """
        The constructor must instantiate the model.
        """
        with patch(self.joystickModelCls) as mockedCtrlrMdl, \
                patch(self.qObject), \
                patch.object(JoystickCtrlr, '_initWidgets'):
            JoystickCtrlr(self.mockedLogger, self.mockedCalBtn,
                          self.mockedJoystickSelect, self.mockedWheelView,
                          self.mockedThrtlBar, self.mockedBrkBar)
            mockedCtrlrMdl.assert_called_once_with(self.mockedLogger)

    def test_constructorInitWidgets(self):
        """
        The constructor must initialize the widgets.
        """
        with patch(self.joystickModelCls), \
                patch(self.qObject), \
                patch.object(JoystickCtrlr, '_initWidgets') \
                as mockedInitWidgets:
            JoystickCtrlr(self.mockedLogger, self.mockedCalBtn,
                          self.mockedJoystickSelect, self.mockedWheelView,
                          self.mockedThrtlBar, self.mockedBrkBar)
            mockedInitWidgets.assert_called_once()

    def test_initWidgetsCalBtn(self):
        """
        The _initWidgets method must connect the calibration button
        to the calibration slots and disable it.
        """
        with patch.object(self.joystickCtrlr, '_initWheelWidgets'):
            self.joystickCtrlr._initWidgets()
            self.mockedCalBtn.clicked.connect. \
                assert_called_once_with(self.mockedJoystickModel.calibrateJoystick)     # noqa: E501

    def test_initWidgetsSelect(self):
        """
        The _initWidgets method must set the combobox model and connect
        the selection change to the activate controller slot.
        """
        with patch.object(self.joystickCtrlr, '_initWheelWidgets'):
            self.joystickCtrlr._initWidgets()
            self.mockedJoystickSelect.setModel. \
                assert_called_once_with(self.mockedJoystickModel.model)
            self.mockedJoystickSelect.currentTextChanged.connect. \
                assert_called_once_with(self.mockedJoystickModel.activateJoystick)      # noqa: E501

    def test_initWidgetsWheel(self):
        """
        The _initWidgets method must initialize the wheel icon widgets.
        """
        with patch.object(self.joystickCtrlr, '_initWheelWidgets') \
                as mockedInitWheelWidgets:
            self.joystickCtrlr._initWidgets()
            mockedInitWheelWidgets.assert_called_once()

    def test_initWidgetsClearAndColorBars(self):
        """
        The _initWidgets method must clear and set the color
        of the throttle and brake bars.
        """
        with patch.object(self.joystickCtrlr, '_initWheelWidgets'):
            self.joystickCtrlr._initWidgets()
            self.mockedThrtlBar.setValue.assert_called_once_with(0)
            self.mockedThrtlBar.setStyleSheet. \
                assert_called_once_with(self.joystickCtrlr.THRTL_STYLESHEET)
            self.mockedBrkBar.setValue.assert_called_once_with(0)
            self.mockedBrkBar.setStyleSheet. \
                assert_called_once_with(self.joystickCtrlr.BRAKE_STYLESHEET)

    def test_initWheelWidgetsCreateScene(self):
        """
        The _initWheelWidgets method must create the graphic scene
        and add the wheel icon to it.
        """
        with patch(self.graphicScene) as mockedGraphScene, \
                patch(self.graphSvgItem) as mockedGraphSvgItem:
            mockedGraphScene.return_value = self.mockedGraphScene
            mockedGraphSvgItem.return_value = self.mockedGraphSvgItem
            self.joystickCtrlr._initWheelWidgets()
            mockedGraphSvgItem. \
                assert_called_once_with(self.joystickCtrlr.WHEEL_ICON)
            self.mockedGraphSvgItem.setScale. \
                assert_called_once_with(self.joystickCtrlr.WHEEL_ICON_SCALE)
            mockedGraphScene.assert_called_once()
            self.mockedGraphScene.addItem. \
                assert_called_once_with(self.mockedGraphSvgItem)
            self.mockedWheelView.setScene. \
                assert_called_once_with(self.mockedGraphScene)

    def test_areJoystickAvailable(self):
        """
        _areJoystickAvailable method must emit an error signal
        only if there are no available joystick.
        """
        retVals = [0, 1]
        self.mockedJoystickModel.model.rowCount.side_effect = retVals
        with patch.object(self.joystickCtrlr, 'error') as mockedErrSignal:
            for retVal in retVals:
                print(retVal)
                self.joystickCtrlr.areJoystickAvailable()
            mockedErrSignal.emit.assert_called_once()
