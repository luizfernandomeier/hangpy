import uuid
from hangpy.dtos.server_configuration_dto import ServerConfigurationDto


class Server():
    """Represents an instance of a HangPy server. Can be instantiated
    multiple times with different configurations for scalability.
    """

    def __init__(self, configuration: ServerConfigurationDto):
        """
        Args:
            configuration (ServerConfigurationDto): An object containing
            the configuration definitions for the instance of a server.
        """
        self.id = str(uuid.uuid4())
        self.start_datetime = None
        self.stop_datetime = None
        self.last_cycle_datetime = None
        self.configuration = configuration
