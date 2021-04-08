import unittest
from freezegun import freeze_time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities import Server


class TestServer(unittest.TestCase):

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_init(self):
        server_configuration = ServerConfigurationDto()
        server = Server(server_configuration)
        self.assertIsNone(server.start_datetime)
        self.assertIsNone(server.stop_datetime)
        self.assertIsNone(server.last_cycle_datetime)
        self.assertEqual(server.configuration, server_configuration)


if (__name__ == "__main__"):
    unittest.main()
