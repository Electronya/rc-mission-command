import logging

from ..messages.unitSteeringMsg import UnitSteeringMessage

class Unit:
    """
    The unit class.
    """
    def __init__(self, id, client):
        """
        Constructor.

        Params:
            id:             The unit ID.
            client:         The MQTT client.
        """
        self._logger = logging.getLogger(f"UNIT_{id.upper()}")
        self._logger.info(f"creating unit with ID: {id}")

        self._id = id
        self._client = client

        self._steeringMsg = UnitSteeringMessage(self._id)

    def _update_steering(self, modifier):
        """
        Update the unit steering.

        Params:
            modifier:       The unit steering modifier.
        """
        self._steeringMsg.update_modifier(modifier)
        self._client.publish(self._steeringMsg.get_topic(),
            payload=self._steeringMsg.to_json())

    def get_id(self):
        """
        Get the unit ID.

        Return:
            The unit ID.
        """
        return self._id

    def get_functions(self):
        """
        Get the unit functions.

        Retrun:
            The unit functions.
        """
        return {
            'steering': self._update_steering,
        }
