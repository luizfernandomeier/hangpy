import datetime
import fakeredis
import redis
import unittest
from freezegun import freeze_time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities.server import Server
from hangpy.repositories.redis_server_repository import RedisServerRepository


class TestRedisServerRepository(unittest.TestCase):

    def test_init(self):
        redis_client = fakeredis.FakeStrictRedis()
        server_repository = RedisServerRepository(redis_client)
        self.assertIsInstance(server_repository.redis_client, redis.StrictRedis)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_add_and_get_servers(self):
        redis_client = fakeredis.FakeStrictRedis()
        server_repository = RedisServerRepository(redis_client)
        fake_server = Server(ServerConfigurationDto())
        server_repository.add_server(fake_server)
        actual_server = server_repository.get_servers()[0]
        expected_server = fake_server

        self.assertNotEqual(actual_server, expected_server)
        self.assertEqual(actual_server.id, expected_server.id)
        self.assertEqual(actual_server.start_datetime, expected_server.start_datetime)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_update_server(self):
        redis_client = fakeredis.FakeStrictRedis()
        server_repository = RedisServerRepository(redis_client)
        fake_server = Server(ServerConfigurationDto())
        server_repository.add_server(fake_server)
        server = server_repository.get_servers()[0]
        server.last_cycle_datetime = datetime.datetime.now().isoformat()
        server_repository.update_server(server)
        actual_server = server_repository.get_servers()[0]

        self.assertEqual(actual_server.last_cycle_datetime, server.last_cycle_datetime)


if (__name__ == '__main__'):
    unittest.main()
