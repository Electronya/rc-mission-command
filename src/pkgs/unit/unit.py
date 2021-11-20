from ..messages import UnitWhldCmdMsg


class Unit:
    """
    The unit class.
    """
    def __init__(self, appLogger: object, client: object, id: str) -> None:
        """
        Constructor.

        Params:
            appLogger:  The application logger.
            client:     The MQTT client.
            id:         The unit ID.
        """
        self._logger = appLogger.getLogger(f"UNIT-{id.upper()}")
        self._logger.info(f"creating unit with ID: {id}")
        self._id = id
        self._client = client
        self._cmdMsg = UnitWhldCmdMsg(self._id)

    def _combineThrtlBrake(self, thrtlModifier: float,
                           brakeModifier: float) -> float:
        """
        Combine the throttle and brake modifier in a single one.

        Params:
            thrtlModifier:  The throttle modifier.
            brakeModifier:  The brake modifier.

        Return:
            The combined modifier.
        """
        modifier = 0.0
        if thrtlModifier > 0 and brakeModifier == 0:
            modifier = thrtlModifier
        if brakeModifier > 0 and thrtlModifier == 0:
            modifier = -1 * brakeModifier
        return modifier

    def getId(self) -> str:
        """
        Get the unit ID.

        Return:
            The unit ID.
        """
        return self._id

    def updateSteeringCmd(self, modifier: float) -> None:
        """
        Update the unit steering command.

        Params:
            modifier:   The unit steering modifier.
        """
        self._cmdMsg.setSteering(modifier)

    def updateThrottleCmd(self, thrtlModifer: float,
                          brakeModifier: float) -> None:
        """
        Update the unit throttle command.

        Params:
            thrtlModifier:  The unit throttle modifier.
            brakeModifier:  The unit brake modifier.
        """
        modifier = self._combineThrtlBrake(thrtlModifer, brakeModifier)
        self._cmdMsg.setThrottle(modifier)

    def sendCommandMsg(self) -> None:
        """
        Send the command message.
        """
        self._client.publish(self._cmdMsg)
