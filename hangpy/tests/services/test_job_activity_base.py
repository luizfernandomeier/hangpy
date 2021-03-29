import unittest
from hangpy.services import JobActivityBase

class TestJobActivityBase(unittest.TestCase):

    def test_start(self):
        global job_action_result
        job_activity = FakeJob()
        job_activity.start()
        expected = "executed the action"
        self.assertEqual(job_action_result, expected)

    def test_get_job_object(self):
        job_activity = FakeJob()
        job = job_activity.get_job_object()
        self.assertTrue(job.module_name.endswith('test_activity_job_base'))
        self.assertEqual(job.class_name, 'FakeJob')

class FakeJob(JobActivityBase):
    def action(self):
        global job_action_result
        job_action_result = "executed the action"

if (__name__ == "__main__"):
    unittest.main()