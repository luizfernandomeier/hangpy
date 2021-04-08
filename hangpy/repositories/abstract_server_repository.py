from abc import ABC, abstractmethod
from hangpy.entities import Server


class AbstractServerRepository(ABC):

    @abstractmethod
    def get_servers(self) -> list[Server]:
        pass

    @abstractmethod
    def add_server(self, server: Server):
        pass

    @abstractmethod
    def update_server(self, server: Server):
        pass
