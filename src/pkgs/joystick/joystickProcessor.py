import pygame as pg
import pygame.event as pgEvent
from PySide2.QtCore import QObject, QRunnable, Signal, Slot


class JoystickProcessSignals(QObject):
    """
    The joystick process signals.
    """
    axisMotion = Signal(int, float)
    hatMotion = Signal(int, float)
    buttonDown = Signal(int)
    buttonUp = Signal(int)


class JoystickProcessor(QRunnable):
    """
    The joystick event processor.

    Params:
        logger:     The joystick logger.
    """

    def __init__(self, logger: object) -> None:
        super().__init__()
        self._logger = logger
        self.signals = JoystickProcessSignals()

    @Slot()
    def run(self):
        """
        The thread execution method
        """
        for ev in pgEvent.get():
            if ev.type == pg.JOYAXISMOTION:
                self._logger.debug(f"processing joystick "
                                   "{ev.instance_id} "
                                   f"axis {ev.axis} with "
                                   f"value {ev.value}")
                self.signals.axisMotion.emit(ev.axis, ev.value)
            if ev.type == pg.JOYBUTTONDOWN:
                self._logger.debug(f"processing joystick "
                                   "{ev.instance_id} "
                                   f"button {ev.button} down")
                self.signals.buttonDown.emit(ev.button)
            if ev.type == pg.JOYBUTTONUP:
                self._logger.debug(f"processing joystick "
                                   "{ev.instance_id} "
                                   f"button {ev.button} up")
                self.signals.buttonUp.emit(ev.button)
            if ev.type == pg.JOYHATMOTION:
                self._logger.debug(f"processing joystick "
                                   "{ev.instance_id} "
                                   f"hat {ev.hat} with value "
                                   f"{ev.value}")
                self.signals.hatMotion.emit(ev.hat, ev.value)
