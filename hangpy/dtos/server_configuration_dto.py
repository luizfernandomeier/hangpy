class ServerConfigurationDto():
    """Class used to manage the server configuration"""

    def __init__(self, cycle_interval_milliseconds: int = 10000, slots: int = 10):
        """
        Args:
            cycle_interval_milliseconds (int, optional): Milliseconds to sleep bewteen the server cycles. Defaults to 10000.
            slots (int, optional): Number os slots available to execute jobs concurrently on each server. Defaults to 10.
        """

        self.__validate_parameters(cycle_interval_milliseconds, slots)
        self.cycle_interval_milliseconds = cycle_interval_milliseconds
        self.slots = slots

    def __validate_parameters(self, cycle_interval_milliseconds: int, slots: int):
        """Internal function used to validate the class constructor parameters."""

        self.__validate_cycle_interval_milliseconds(cycle_interval_milliseconds)
        self.__validate_slots(slots)

    def __validate_cycle_interval_milliseconds(self, cycle_interval_milliseconds: int):
        """
        Internal function used to validate the 'cycle_interval_milliseconds' value.

        Raises:
            ValueError: The value must be an integer
            ValueError: The value must be greater than zero
        """

        if (not isinstance(cycle_interval_milliseconds, int)):
            raise ValueError('cycle_interval_milliseconds', cycle_interval_milliseconds, 'The value must be an integer')
        if (cycle_interval_milliseconds <= 0):
            raise ValueError('cycle_interval_milliseconds', cycle_interval_milliseconds, 'The value must be greater than zero')

    def __validate_slots(self, slots: int):
        """
        Internal function used to validate the 'slots' value.

        Raises:
            ValueError: The value must be an integer
            ValueError: The value must be greater than zero
        """

        if (not isinstance(slots, int)):
            raise ValueError('slots', slots, 'The value must be an integer')
        if (slots <= 0):
            raise ValueError('slots', slots, 'The value must be greater than zero')
