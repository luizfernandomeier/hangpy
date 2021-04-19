import datetime
import fakeredis
import redis
import unittest
from freezegun import freeze_time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities.server import Server
from hangpy.repositories.redis_server_repository import RedisServerRepository


class TestRedisServerRepository(unittest.TestCase):

    def setUp(self):
        redis_client = fakeredis.FakeStrictRedis()
        self.server_repository = RedisServerRepository(redis_client)

    def setUp_fake_server(self):
        self.fake_server = Server(ServerConfigurationDto())

    def add_fake_server_to_repository(self):
        self.server_repository.add_server(self.fake_server)

    def test_init(self):
        self.assertIsInstance(self.server_repository.redis_client, redis.StrictRedis)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_add_and_get_servers(self):
        self.setUp_fake_server()
        self.add_fake_server_to_repository()
        actual_server = self.server_repository.get_servers()[0]
        self.assertNotEqual(actual_server, self.fake_server)
        self.assertEqual(actual_server.id, self.fake_server.id)
        self.assertEqual(actual_server.start_datetime, self.fake_server.start_datetime)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_update_server(self):
        self.setUp_fake_server()
        self.add_fake_server_to_repository()
        self.fake_server.last_cycle_datetime = datetime.datetime.now().isoformat()
        self.server_repository.update_server(self.fake_server)
        actual_server = self.server_repository.get_servers()[0]
        self.assertEqual(actual_server.last_cycle_datetime, self.fake_server.last_cycle_datetime)


if (__name__ == '__main__'):
    unittest.main()
