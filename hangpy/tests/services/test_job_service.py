import types
from hangpy.entities import Job
from hangpy.services import JobService
from unittest import TestCase, mock, main


class TestJobService(TestCase):

    def test_enqueue_job(self):
        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.add_job = mock.MagicMock()
        job_service = JobService(fake_job_repository)
        job = Job('module_test', 'class_test')
        self.assertEqual(fake_job_repository.add_job.call_count, 0)
        job_service.enqueue_job(job)
        self.assertEqual(fake_job_repository.add_job.call_count, 1)


if (__name__ == "__main__"):
    main()
