import unittest
from freezegun import freeze_time
from hangpy.entities import Job
from hangpy.enums import JobStatus


class TestJob(unittest.TestCase):

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_init_with_parameters(self):
        job = Job('module1', 'class2', ['param3', 'param4'])
        self.assertEqual(job.module_name, 'module1')
        self.assertEqual(job.class_name, 'class2')
        self.assertEqual(job.status, JobStatus.ENQUEUED)
        self.assertEqual(job.enqueued_datetime, '1988-04-10T11:01:02.123456')
        self.assertIsNone(job.start_datetime)
        self.assertIsNone(job.end_datetime)
        self.assertListEqual(job.parameters, ['param3', 'param4'])

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_init_without_parameters(self):
        job = Job('module1', 'class2')
        self.assertEqual(job.module_name, 'module1')
        self.assertEqual(job.class_name, 'class2')
        self.assertEqual(job.status, JobStatus.ENQUEUED)
        self.assertIsNone(job.error)
        self.assertEqual(job.enqueued_datetime, '1988-04-10T11:01:02.123456')
        self.assertIsNone(job.start_datetime)
        self.assertIsNone(job.end_datetime)
        self.assertListEqual(job.parameters, [])

    def test_init_with_invalid_module_name(self):
        with self.assertRaises(ValueError):
            Job('', 'class2')

        with self.assertRaises(ValueError):
            Job(123, 'class2')

    def test_init_with_invalid_class_name(self):
        with self.assertRaises(ValueError):
            Job('module1', '')

        with self.assertRaises(ValueError):
            Job('module1', 123)

    def test_init_with_invalid_parameters(self):
        with self.assertRaises(ValueError):
            Job('module1', 'class2', 123)

        with self.assertRaises(ValueError):
            Job('module1', 'class2', 'text')

        with self.assertRaises(ValueError):
            Job('module1', 'class2', range(10))


if (__name__ == "__main__"):
    unittest.main()
