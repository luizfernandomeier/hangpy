import unittest
from hangpy.enums import JobStatus


class TestJobStatus(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(JobStatus.ENQUEUED.value, 0)
        self.assertEqual(JobStatus.PROCESSING.value, 10)
        self.assertEqual(JobStatus.SUCCESS.value, 20)
        self.assertEqual(JobStatus.ERROR.value, 99)


if (__name__ == "__main__"):
    unittest.main()
