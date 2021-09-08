from ..messages.unitWhldCmdMsg import UnitWhldCmdMsg


class Unit:
    """
    The unit class.
    """
    def __init__(self, appLogger: object, client: object, id: str) -> None:
        """
        Constructor.

        Params:
            appLogger:      The application logger.
            client:         The MQTT client.
            id:             The unit ID.
        """
        self._logger = appLogger.getLogger(f"UNIT-{id.upper()}")
        self._logger.info(f"creating unit with ID: {id}")
        self._id = id
        self._client = client
        self._steeringMsg = UnitWhldCmdMsg(self._id)

    def getId(self):
        """
        Get the unit ID.

        Return:
            The unit ID.
        """
        return self._id

    def _update_steering(self, modifier):
        """
        Update the unit steering.

        Params:
            modifier:       The unit steering modifier.
        """
        self._steeringMsg.update_modifier(modifier)
        self._client.publish(self._steeringMsg.get_topic(),
                             payload=self._steeringMsg.to_json())
