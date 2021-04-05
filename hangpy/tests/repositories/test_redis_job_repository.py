import fakeredis
import hangpy.tests.fake as fake
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
        fake_job = fake.FakeJob()
        job_repository.add_job(fake_job)
        actual_job = job_repository.get_jobs()[0]
        expected_job = fake_job.get_job_object()

        self.assertEqual(actual_job.module_name, expected_job.module_name)
        self.assertEqual(actual_job.class_name, expected_job.class_name)
        self.assertListEqual(actual_job.parameters, expected_job.parameters)

    def test_get_jobs_by_status(self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        fake_job = fake.FakeJob()
        job_repository.add_job(fake_job)

        actual_job = job_repository.get_jobs_by_status(JobStatus.ENQUEUED)[0]
        expected_job = fake_job.get_job_object()
        self.assertEqual(actual_job.module_name, expected_job.module_name)
        self.assertEqual(actual_job.class_name, expected_job.class_name)
        self.assertListEqual(actual_job.parameters, expected_job.parameters)

        job = actual_job
        job.status = JobStatus.PROCESSING
        job_repository.update_job(job)

        actual_jobs = job_repository.get_jobs_by_status(JobStatus.ENQUEUED)
        expected_jobs = []
        self.assertListEqual(actual_jobs, expected_jobs)

        actual_job = job_repository.get_jobs_by_status(JobStatus.PROCESSING)[0]
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
        fake_job = fake.FakeJob()
        job_repository.add_job(fake_job)
        job = job_repository.get_jobs()[0]
        job.parameters.append('luiz')
        job.status = JobStatus.ERROR
        job_repository.update_job(job)
        actual_job = job_repository.get_jobs()[0]

        self.assertListEqual(actual_job.parameters, ['luiz'])
        self.assertEqual(actual_job.status, JobStatus.ERROR)
    
    def test_update_jobs(self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        fake_job1 = fake.FakeJob()
        fake_job2 = fake.FakeJob()
        job_repository.add_job(fake_job1)
        job_repository.add_job(fake_job2)
        jobs = job_repository.get_jobs()
        jobs[0].parameters.append('luiz')
        jobs[1].parameters.append('fernando')
        jobs[0].status = JobStatus.ERROR
        jobs[1].status = JobStatus.PROCESSING
        job_repository.update_jobs(jobs)
        actual_jobs = job_repository.get_jobs()

        self.assertListEqual(actual_jobs[0].parameters, ['luiz'])
        self.assertListEqual(actual_jobs[1].parameters, ['fernando'])
        self.assertEqual(actual_jobs[0].status, JobStatus.ERROR)
        self.assertEqual(actual_jobs[1].status, JobStatus.PROCESSING)

    def test_try_set_lock_on_job(self):
        redis_client = fakeredis.FakeStrictRedis()
        job_repository = RedisJobRepository(redis_client)
        fake_job1 = fake.FakeJob()
        fake_job2 = fake.FakeJob()
        job_repository.add_job(fake_job1)
        job_repository.add_job(fake_job2)
        jobs = job_repository.get_jobs()

        actual_lock_set = job_repository.try_set_lock_on_job(jobs[0])
        self.assertTrue(actual_lock_set)

        actual_lock_set = job_repository.try_set_lock_on_job(jobs[0])
        self.assertFalse(actual_lock_set)

        actual_lock_set = job_repository.try_set_lock_on_job(jobs[0])
        self.assertFalse(actual_lock_set)

        actual_lock_set = job_repository.try_set_lock_on_job(jobs[1])
        self.assertTrue(actual_lock_set)

        actual_lock_set = job_repository.try_set_lock_on_job(jobs[1])
        self.assertFalse(actual_lock_set)

if (__name__ == '__main__'):
    unittest.main()