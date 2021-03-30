import fakeredis
import redis
import unittest
from hangpy.enums.job_status import JobStatus
from hangpy.repositories.redis_job_repository import RedisJobRepository
from hangpy.services import JobActivityBase

class TestRedisJobRepository(unittest.TestCase):

    def test_init (self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        self.assertIsInstance(job_repository.redis_client, redis.StrictRedis)

    def test_add_and_get_jobs(self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        fake_job = FakeJob()
        job_repository.add_job(fake_job)
        actual_job = job_repository.get_jobs()[0]
        expected_job = fake_job.get_job_object()

        self.assertEqual(actual_job.module_name, expected_job.module_name)
        self.assertEqual(actual_job.class_name, expected_job.class_name)
        self.assertListEqual(actual_job.parameters, expected_job.parameters)

    def test_get_jobs_by_status(self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        fake_job = FakeJob()
        job_repository.add_job(fake_job)
        actual_job = job_repository.get_jobs_by_status(JobStatus.ENQUEUED)[0]
        expected_job = fake_job.get_job_object()

        self.assertEqual(actual_job.module_name, expected_job.module_name)
        self.assertEqual(actual_job.class_name, expected_job.class_name)
        self.assertListEqual(actual_job.parameters, expected_job.parameters)

        actual_jobs = job_repository.get_jobs_by_status(JobStatus.SUCCESS)
        expected_jobs = []

        self.assertListEqual(actual_jobs, expected_jobs)

    def test_update_job(self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        fake_job = FakeJob()
        job_repository.add_job(fake_job)
        job = job_repository.get_jobs()[0]
        job.parameters.append('luiz')
        job.status = JobStatus.ERROR
        job_repository.update_job(job)
        actual_job = job_repository.get_jobs()[0]

        self.assertListEqual(actual_job.parameters, ['luiz'])
        self.assertEqual(actual_job.status, JobStatus.ERROR)

class FakeJob(JobActivityBase):
    pass

if (__name__ == '__main__'):
    unittest.main()