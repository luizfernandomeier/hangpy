import types
from hangpy.services import JobService
from unittest import TestCase, mock, main


class TestJobService(TestCase):

    def test_enqueue_job(self):
        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.add_job = mock.MagicMock()
        fake_job_activity = types.SimpleNamespace()
        fake_job_activity.create_job_object = mock.MagicMock()
        job_service = JobService(fake_job_repository)
        self.assertEqual(fake_job_activity.create_job_object.call_count, 0)
        self.assertEqual(fake_job_repository.add_job.call_count, 0)
        job_service.enqueue_job(fake_job_activity)
        self.assertEqual(fake_job_activity.create_job_object.call_count, 1)
        self.assertEqual(fake_job_repository.add_job.call_count, 1)

        job_service.enqueue_job(fake_job_activity, ['a', 'b'])
        actual_args = fake_job_activity.create_job_object.call_args[0][0]
        self.assertListEqual(actual_args, ['a', 'b'])


if (__name__ == "__main__"):
    main()
