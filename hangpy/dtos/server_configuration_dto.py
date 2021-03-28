class ServerConfigurationDto():

    def __init__(self, cycle_interval_milliseconds=10000):
        self.__validate_parameters(cycle_interval_milliseconds)
        self.cycle_interval_milliseconds = cycle_interval_milliseconds

    def __validate_parameters(self, cycle_interval_milliseconds):
        self.__validate_cycle_interval_milliseconds(cycle_interval_milliseconds)

    def __validate_cycle_interval_milliseconds(self, cycle_interval_milliseconds):
        if (not isinstance(cycle_interval_milliseconds, int)):
            raise ValueError('cycle_interval_milliseconds', cycle_interval_milliseconds, 'The value must be an integer')
        if (cycle_interval_milliseconds <= 0):
            raise ValueError('cycle_interval_milliseconds', cycle_interval_milliseconds, 'The value must be greater than zero')