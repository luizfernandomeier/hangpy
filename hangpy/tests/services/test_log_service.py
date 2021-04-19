import unittest
from hangpy.services import LogService


class TestLogService(unittest.TestCase):

    def test_instantiate(self):
        log_service = FakeLogService()
        self.assertIsNone(log_service.log(None))


class FakeLogService(LogService):

    def log(self, message):
        return LogService.log(self, message)


if (__name__ == "__main__"):
    unittest.main()
