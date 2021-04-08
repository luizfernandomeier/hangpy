from abc import ABC, abstractmethod


class AbstractServerRepository(ABC):

    @abstractmethod
    def get_servers(self):
        pass

    @abstractmethod
    def add_server(self, server):
        pass

    @abstractmethod
    def update_server(self, server):
        pass
