import unittest
from hangpy.dtos import ServerConfigurationDto


class TestServerConfigurationDto(unittest.TestCase):

    def test_init_with_default_values(self):
        server_configuration = ServerConfigurationDto()
        self.assertEqual(server_configuration.cycle_interval_milliseconds, 10000)
        self.assertEqual(server_configuration.slots, 10)

    def test_init_with_custom_values(self):
        server_configuration = ServerConfigurationDto(500, 5)
        self.assertEqual(server_configuration.cycle_interval_milliseconds, 500)
        self.assertEqual(server_configuration.slots, 5)

    def test_init_with_invalid_cycle_interval_milliseconds(self):
        with self.assertRaises(ValueError):
            ServerConfigurationDto(cycle_interval_milliseconds=1.1)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(cycle_interval_milliseconds=-1)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(cycle_interval_milliseconds=0)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(cycle_interval_milliseconds=None)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(cycle_interval_milliseconds='x')

    def test_init_with_invalid_slots(self):
        with self.assertRaises(ValueError):
            ServerConfigurationDto(slots=1.1)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(slots=-1)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(slots=0)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(slots=None)

        with self.assertRaises(ValueError):
            ServerConfigurationDto(slots='x')


if (__name__ == "__main__"):
    unittest.main()
