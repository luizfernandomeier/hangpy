import jsonpickle
import redis
from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import AbstractServerRepository

class RedisServerRepository(AbstractServerRepository, RedisRepositoryBase):

    def __init__(self, host, port, password=None):
        RedisRepositoryBase.__init__(self, host, port, password)

    def get_servers(self):
        keys = self._get_keys('server.*')
        serialized_servers = self.client.mget(keys)
        return self._deserialize_entries(serialized_servers)
    
    def add_server(self, server):
        self.__set_server(server)

    def update_server(self, server):
        self.__set_server(server)

    def __set_server(self, server):
        serialized_server = jsonpickle.encode(server)
        self.client.set(f'server.{server.id}', serialized_server)