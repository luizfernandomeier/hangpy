import unittest
from hangpy.dtos import ServerConfigurationDto


class TestServerConfigurationDto(unittest.TestCase):

    def test_init(self):

        server_configuration = ServerConfigurationDto()
        self.assertEqual(server_configuration.cycle_interval_milliseconds, 10000)
        self.assertEqual(server_configuration.slots, 10)

        server_configuration = ServerConfigurationDto(500, 5)
        self.assertEqual(server_configuration.cycle_interval_milliseconds, 500)
        self.assertEqual(server_configuration.slots, 5)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(cycle_interval_milliseconds=1.1)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(cycle_interval_milliseconds=-1)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(cycle_interval_milliseconds=0)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(cycle_interval_milliseconds=None)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(cycle_interval_milliseconds='x')

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(slots=1.1)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(slots=-1)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(slots=0)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(slots=None)

        with self.assertRaises(ValueError):
            server_configuration = ServerConfigurationDto(slots='x')


if (__name__ == "__main__"):
    unittest.main()
