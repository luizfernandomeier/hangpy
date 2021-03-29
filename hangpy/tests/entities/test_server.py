import datetime
import unittest
from freezegun import freeze_time
from hangpy.entities import Server

class TestServer(unittest.TestCase):

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_init(self):
        server = Server()
        self.assertEqual(server.start_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(server.stop_datetime, None)
        self.assertEqual(server.last_cycle_datetime, None)

if (__name__ == "__main__"):
    unittest.main()