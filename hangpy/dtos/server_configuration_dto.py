class ServerConfigurationDto():
    """Class used to group the server configuration
    """

    def __init__(self, cycle_interval_milliseconds: int = 10000):
        """
        Args:
            cycle_interval_milliseconds (int, optional): Milliseconds to sleep bewteen the server cycles.
            Defaults to 10000.
        """
        self.__validate_parameters(cycle_interval_milliseconds)
        self.cycle_interval_milliseconds = cycle_interval_milliseconds

    def __validate_parameters(self, cycle_interval_milliseconds: int):
        """Internal method used to validate the class constructor parameters.

        Args:
            cycle_interval_milliseconds (int, optional): Milliseconds to sleep bewteen the server cycles.
        """
        self.__validate_cycle_interval_milliseconds(cycle_interval_milliseconds)

    def __validate_cycle_interval_milliseconds(self, cycle_interval_milliseconds: int):
        """Internal method used to validate the cycle_interval_milliseconds value.

        Args:
            cycle_interval_milliseconds ([type]): Milliseconds to sleep bewteen the server cycles.

        Raises:
            ValueError: The value must be an integer
            ValueError: The value must be greater than zero
        """
        if (not isinstance(cycle_interval_milliseconds, int)):
            raise ValueError('cycle_interval_milliseconds', cycle_interval_milliseconds, 'The value must be an integer')
        if (cycle_interval_milliseconds <= 0):
            raise ValueError('cycle_interval_milliseconds', cycle_interval_milliseconds, 'The value must be greater than zero')
