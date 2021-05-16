import logging

class Unit:
    """
    The unit class.
    """
    def __init__(self, id):
        """
        Constructor.

        Params:
            id:         The unit ID.
        """
        self._logger = logging.getLogger(f"UNIT_{id.upper()}")
        self._logger.info(f"creating unit with ID: {id}")

        self._id = id

    def get_id(self):
        """
        Get the unit ID.

        Return:
            The unit ID.
        """
        return self._id
