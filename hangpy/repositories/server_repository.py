from abc import ABC, abstractmethod
from hangpy.entities import Server


class ServerRepository(ABC):
    """
    Interface defining the functions necessary for a class to be used as
    server repository.
    """

    @abstractmethod
    def get_servers(self) -> list[Server]:
        pass

    @abstractmethod
    def add_server(self, server: Server):
        pass

    @abstractmethod
    def update_server(self, server: Server):
        pass
