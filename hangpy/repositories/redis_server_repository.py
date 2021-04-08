from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import AbstractServerRepository


class RedisServerRepository(AbstractServerRepository, RedisRepositoryBase):

    def __init__(self, redis_client):
        RedisRepositoryBase.__init__(self, redis_client)

    def get_servers(self):
        keys = self._get_keys('server.*')
        serialized_servers = self.redis_client.mget(keys)
        return self._deserialize_entries(serialized_servers)

    def add_server(self, server):
        self.__set_server(server)

    def update_server(self, server):
        self.__set_server(server)

    def __set_server(self, server):
        serialized_server = self._serialize_entry(server)
        self.redis_client.set(f'server.{server.id}', serialized_server)
