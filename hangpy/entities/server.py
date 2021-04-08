import uuid
from hangpy.dtos.server_configuration_dto import ServerConfigurationDto


class Server():

    def __init__(self, configuration: ServerConfigurationDto):
        self.id = str(uuid.uuid4())
        self.start_datetime = None
        self.stop_datetime = None
        self.last_cycle_datetime = None
        self.configuration = configuration
