import fakeredis
import hangpy.tests.fake as fake
import redis
import unittest
from hangpy.enums.job_status import JobStatus
from hangpy.repositories.redis_job_repository import RedisJobRepository


class FakeRedisTestGetNone(fakeredis.FakeStrictRedis):
    def get(self, key):
        return None


class TestRedisJobRepository(unittest.TestCase):

    def setUp(self):
        redis_client = fakeredis.FakeStrictRedis()
        self.job_repository = RedisJobRepository(redis_client)

    def setUp_fake_job(self):
        self.fake_job = fake.FakeJobActivity().create_job_object()

    def setUp_fake_jobs(self):
        self.fake_job1 = fake.FakeJobActivity().create_job_object()
        self.fake_job2 = fake.FakeJobActivity().create_job_object()

    def add_fake_job_to_repository(self):
        self.job_repository.add_job(self.fake_job)

    def add_fake_jobs_to_repository(self):
        self.job_repository.add_job(self.fake_job1)
        self.job_repository.add_job(self.fake_job2)

    def test_init(self):
        self.assertIsInstance(self.job_repository.redis_client, redis.StrictRedis)

    def test_add_and_get_jobs(self):
        self.setUp_fake_job()
        self.add_fake_job_to_repository()
        actual_job = self.job_repository.get_jobs()[0]
        self.assertEqual(actual_job.module_name, self.fake_job.module_name)
        self.assertEqual(actual_job.class_name, self.fake_job.class_name)
        self.assertListEqual(actual_job.parameters, self.fake_job.parameters)

    def test_get_job_by_status_returning_job_enqueued(self):
        self.setUp_fake_job()
        self.add_fake_job_to_repository()
        actual_job = self.job_repository.get_job_by_status(JobStatus.ENQUEUED)
        self.assertEqual(actual_job.module_name, self.fake_job.module_name)
        self.assertEqual(actual_job.class_name, self.fake_job.class_name)
        self.assertListEqual(actual_job.parameters, self.fake_job.parameters)

    def test_get_job_by_status_returning_none(self):
        self.setUp_fake_job()
        self.fake_job.status = JobStatus.PROCESSING
        self.add_fake_job_to_repository()
        actual_job = self.job_repository.get_job_by_status(JobStatus.ENQUEUED)
        self.assertIsNone(actual_job)

    def test_get_job_by_status_returning_job_success(self):
        self.setUp_fake_job()
        self.fake_job.status = JobStatus.SUCCESS
        self.add_fake_job_to_repository()
        actual_job = self.job_repository.get_job_by_status(JobStatus.SUCCESS)
        self.assertEqual(actual_job.module_name, self.fake_job.module_name)
        self.assertEqual(actual_job.class_name, self.fake_job.class_name)
        self.assertListEqual(actual_job.parameters, self.fake_job.parameters)

    def test_get_job_by_status_with_orphan_key(self):
        redis_client = FakeRedisTestGetNone()
        job_repository = RedisJobRepository(redis_client)
        redis_client.set(F'jobstatus:ABCDE:{str(JobStatus.ENQUEUED)}', 'some_key_that_doesnt_exist')
        actual_job = job_repository.get_job_by_status(JobStatus.ENQUEUED)
        self.assertIsNone(actual_job)

    def test_get_jobs_by_status_returning_job_enqueued(self):
        self.setUp_fake_job()
        self.add_fake_job_to_repository()
        actual_job = self.job_repository.get_jobs_by_status(JobStatus.ENQUEUED)[0]
        self.assertEqual(actual_job.module_name, self.fake_job.module_name)
        self.assertEqual(actual_job.class_name, self.fake_job.class_name)
        self.assertListEqual(actual_job.parameters, self.fake_job.parameters)

    def test_get_job_by_status_returning_empty_list(self):
        self.setUp_fake_job()
        self.fake_job.status = JobStatus.PROCESSING
        self.add_fake_job_to_repository()
        actual_jobs = self.job_repository.get_jobs_by_status(JobStatus.ENQUEUED)
        self.assertListEqual(actual_jobs, [])

    def test_get_jobs_by_status_returning_job_success(self):
        self.setUp_fake_job()
        self.fake_job.status = JobStatus.SUCCESS
        self.add_fake_job_to_repository()
        actual_job = self.job_repository.get_jobs_by_status(JobStatus.SUCCESS)[0]
        self.assertEqual(actual_job.module_name, self.fake_job.module_name)
        self.assertEqual(actual_job.class_name, self.fake_job.class_name)
        self.assertListEqual(actual_job.parameters, self.fake_job.parameters)

    def test_exists_jobs_with_status(self):
        self.setUp_fake_job()
        self.add_fake_job_to_repository()
        self.assertTrue(self.job_repository.exists_jobs_with_status(JobStatus.ENQUEUED))
        self.assertFalse(self.job_repository.exists_jobs_with_status(JobStatus.PROCESSING))

    def test_update_job(self):
        self.setUp_fake_job()
        self.add_fake_job_to_repository()
        self.fake_job.parameters.append('luiz')
        self.fake_job.status = JobStatus.ERROR
        self.job_repository.update_job(self.fake_job)
        actual_job = self.job_repository.get_jobs()[0]
        self.assertListEqual(actual_job.parameters, ['luiz'])
        self.assertEqual(actual_job.status, JobStatus.ERROR)

    def test_update_jobs(self):
        self.setUp_fake_jobs()
        self.add_fake_jobs_to_repository()
        self.fake_job1.parameters.append('luiz')
        self.fake_job2.parameters.append('fernando')
        self.fake_job1.status = JobStatus.ERROR
        self.fake_job2.status = JobStatus.PROCESSING
        self.fake_job1.test_sequence = 1
        self.fake_job2.test_sequence = 2
        self.job_repository.update_jobs([self.fake_job1, self.fake_job2])
        actual_jobs = sorted(self.job_repository.get_jobs(), key=lambda x: x.test_sequence)
        self.assertListEqual(actual_jobs[0].parameters, ['luiz'])
        self.assertListEqual(actual_jobs[1].parameters, ['fernando'])
        self.assertEqual(actual_jobs[0].status, JobStatus.ERROR)
        self.assertEqual(actual_jobs[1].status, JobStatus.PROCESSING)

    def test_try_set_lock_on_job(self):
        self.setUp_fake_jobs()
        self.add_fake_jobs_to_repository()
        self.assertTrue(self.job_repository.try_set_lock_on_job(self.fake_job1))
        self.assertFalse(self.job_repository.try_set_lock_on_job(self.fake_job1))
        self.assertFalse(self.job_repository.try_set_lock_on_job(self.fake_job1))
        self.assertTrue(self.job_repository.try_set_lock_on_job(self.fake_job2))
        self.assertFalse(self.job_repository.try_set_lock_on_job(self.fake_job2))


if (__name__ == '__main__'):
    unittest.main()
