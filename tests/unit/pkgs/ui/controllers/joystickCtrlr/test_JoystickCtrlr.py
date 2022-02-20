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
        self.messageBox = 'pkgs.ui.controllers.joystickCtrlr.joystickCtrlr.QMessageBox'             # noqa: E501
        self.transform = 'pkgs.ui.controllers.joystickCtrlr.joystickCtrlr.QTransform'               # noqa: E501
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
        mockedModel = Mock()
        with patch(self.joystickModelCls) as mockedCtrlrMdl, \
                patch(self.qObject), \
                patch.object(JoystickCtrlr, '_initWidgets'):
            mockedCtrlrMdl.return_value = mockedModel
            JoystickCtrlr(self.mockedLogger, self.mockedCalBtn,
                          self.mockedJoystickSelect, self.mockedWheelView,
                          self.mockedThrtlBar, self.mockedBrkBar)
            mockedCtrlrMdl.assert_called_once_with(self.mockedLogger)
            mockedModel.calibration.connect.assert_called_once()
            mockedModel.axisMotion.connect.assert_called_once()

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
        to the calibration slots.
        """
        expectedState = True
        self.mockedJoystickModel \
            .isJoystickCalibrated.return_value = expectedState
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
                assert_called_once_with(self.joystickCtrlr._switchJoystick)

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

    def test_createCalibMsgBoxCreateMsgBx(self):
        """
        The _createCalibMsgBox method must create and display
        the calibration message box with the received message.
        """
        expectedMsg = 'test message'
        mockedMsgBox = Mock()
        with patch(self.messageBox) as mockedMsgBoxConst:
            mockedMsgBoxConst.return_value = mockedMsgBox
            self.joystickCtrlr._createCalibMsgBox(expectedMsg)
            mockedMsgBoxConst.assert_called_once()
            mockedMsgBox.setWindowTitle.assert_called_once()
            mockedMsgBox.setText.assert_called_once_with(expectedMsg)
            mockedMsgBox.setIcon.assert_called_once()
            mockedMsgBox.exec_.assert_called_once()

    def test_createCalibMsgBoxNextSequence(self):
        """
        The _createCalibMsgBox method must go to the next
        calibration sequence.
        """
        with patch(self.messageBox):
            self.joystickCtrlr._createCalibMsgBox('TEST')
            self.mockedJoystickModel.calibrateJoystick.assert_called_once()

    def test_createCalibMsgBoxDone(self):
        """
        The _createCalibMsgBox method must disable the calibration
        button if the calibration process is done.
        """
        with patch(self.messageBox):
            self.joystickCtrlr._createCalibMsgBox('hdhdh done oofid')
            self.mockedCalBtn.setEnabled.assert_called_once_with(False)

    def test_switchJoystickActivateJoystick(self):
        """
        The _switchJoystick method must activate the newly
        selected joystick.
        """
        newJoystick = 'new joystick'
        self.joystickCtrlr._switchJoystick(newJoystick)
        self.mockedJoystickModel.activateJoystick \
            .assert_called_once_with(newJoystick)

    def test_switchJoystickCalibBtnEnState(self):
        """
        The _switchJoystick method must set the calibration button
        enable state base on the newly activated joystick
        calibration state.
        """
        newJoystick = 'new joystick'
        calibStates = (True, False)
        self.mockedJoystickModel.isJoystickCalibrated.side_effect = calibStates
        for calibState in calibStates:
            self.joystickCtrlr._switchJoystick(newJoystick)
            self.mockedCalBtn.setEnabled \
                .assert_called_with(not calibState)

    def test_updateSteering(self):
        """
        The _updateSteering method must update the wheel widget
        transform.
        """
        testMods = (-1.0, -0.75, 0.0, 0.34, 1.0)
        mockedTransform = Mock()
        for testMod in testMods:
            with patch(self.transform) as mockedTransformConst:
                mockedTransformConst.return_value = mockedTransform
                self.joystickCtrlr._updateSteering(testMod)
                mockedTransformConst.assert_called_once()
                mockedTransform.rotate.assert_called_with(180 * testMod)
                self.mockedWheelView.setTransform \
                    .assert_called_with(mockedTransform)

    def test_updateThrottle(self):
        """
        The _updateThrottle method must update the throttle widget.
        """
        testMods = (0.0, 0.26, 0.68, 1.0)
        testMin = 0
        testMax = 100
        testRange = testMax - testMin
        for testMod in testMods:
            self.mockedThrtlBar.minimum.return_value = testMin
            self.mockedThrtlBar.maximum.return_value = testMax
            self.joystickCtrlr._updateThrottle(testMod)
            self.mockedThrtlBar.setValue \
                .assert_called_with(int((testRange * testMod) + testMin))

    def test_updateBrake(self):
        """
        The _updateBrake method must update the brake widget.
        """
        testMods = (0.0, 0.26, 0.68, 1.0)
        testMin = 0
        testMax = 100
        testRange = testMax - testMin
        for testMod in testMods:
            self.mockedBrkBar.minimum.return_value = testMin
            self.mockedBrkBar.maximum.return_value = testMax
            self.joystickCtrlr._updateBrake(testMod)
            self.mockedBrkBar.setValue \
                .assert_called_with(int((testRange * testMod) + testMin))

    def test_axisMotionCallbackUpdateWidgets(self):
        """
        The _axisMotionCallback method must update the widget link the
        axis being moved.
        """
        testVals = (
            {'type': 'steering wheel', 'axis': 0, 'mod': -0.25},
            {'type': 'steering wheel', 'axis': 1, 'mod': 0.49},
            {'type': 'steering wheel', 'axis': 2, 'mod': 0.82},
        )
        with patch.object(self.joystickCtrlr, '_updateSteering') \
                as mockedUpdateSteering, \
                patch.object(self.joystickCtrlr, '_updateThrottle') \
                as mockedUpdateThrtl, \
                patch.object(self.joystickCtrlr, '_updateBrake') \
                as mockedUpdateBrake:
            testVals[0]['update'] = mockedUpdateSteering
            testVals[1]['update'] = mockedUpdateThrtl
            testVals[2]['update'] = mockedUpdateBrake
            for testVal in testVals:
                self.joystickCtrlr._axisMotionCallback(testVal['type'],
                                                       testVal['axis'],
                                                       testVal['mod'])
                testVal['update'].assert_called_once_with(testVal['mod'])

    def test_areJoystickAvailableNoJoystick(self):
        """
        The _areJoystickAvailable method must emit an error signal
        only if there are no available joystick and set the
        calibration button enabled state base on the calibration
        state of the active joystick.
        """
        retVals = [0, 1]
        self.mockedJoystickModel.model.rowCount.side_effect = retVals
        self.mockedJoystickModel.isJoystickCalibrated \
            .side_effect = (False, False)
        with patch.object(self.joystickCtrlr, 'error') as mockedErrSignal:
            for retVal in retVals:
                print(retVal)
                self.joystickCtrlr.areJoystickAvailable()
            mockedErrSignal.emit.assert_called_once()
            self.mockedCalBtn.setEnabled.assert_called_once_with(not False)
