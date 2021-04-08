from hangpy.entities import Server
from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import AbstractServerRepository
from redis import Redis


class RedisServerRepository(AbstractServerRepository, RedisRepositoryBase):
    """Implementation of the AbstractServerRepository using Redis."""

    def __init__(self, redis_client: Redis):
        """
        Args:
            redis_client (Redis): Implementation of a Redis client.
        """
        RedisRepositoryBase.__init__(self, redis_client)

    def get_servers(self) -> list[Server]:
        keys = self._get_keys('server.*')
        serialized_servers = self.redis_client.mget(keys)
        return self._deserialize_entries(serialized_servers)

    def add_server(self, server: Server):
        self.__set_server(server)

    def update_server(self, server: Server):
        self.__set_server(server)

    def __set_server(self, server: Server):
        """Internal function to unify the command 'set' used for both add and
        update instructions on Redis.

        Args:
            server (Server)
        """
        serialized_server = self._serialize_entry(server)
        self.redis_client.set(f'server.{server.id}', serialized_server)
