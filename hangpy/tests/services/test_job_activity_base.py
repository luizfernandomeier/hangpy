import hangpy.tests.fake as fake
import unittest
from hangpy.services import JobActivityBase

class TestJobActivityBase(unittest.TestCase):

    def test_action(self):
        fake_abstract_job = fake.FakeAbstractJob()
        self.assertIsNone(fake_abstract_job.action())

    def test_start(self):
        fake.fake_job_action_result = None
        job_activity = fake.FakeJob()
        job_activity.start()
        expected = "executed the action"
        self.assertEqual(fake.fake_job_action_result, expected)

    def test_get_job_object(self):
        job_activity = fake.FakeJob()
        job = job_activity.get_job_object()
        self.assertTrue(job.module_name.endswith('fake'))
        self.assertEqual(job.class_name, 'FakeJob')

if (__name__ == "__main__"):
    unittest.main()