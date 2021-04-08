import unittest
from hangpy.dtos import ServerConfigurationDto


class TestServerConfigurationDto(unittest.TestCase):

    def test_init(self):

        server_configuration = ServerConfigurationDto()
        self.assertEqual(server_configuration.cycle_interval_milliseconds, 10000)

        server_configuration = ServerConfigurationDto(500)
        self.assertEqual(server_configuration.cycle_interval_milliseconds, 500)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(1.1)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(-1)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(0)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(None)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto('x')


if (__name__ == "__main__"):
    unittest.main()
