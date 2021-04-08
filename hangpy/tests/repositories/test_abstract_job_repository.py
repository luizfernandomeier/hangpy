import unittest
from hangpy.repositories import AbstractJobRepository


class TestAbstractJobRepository(unittest.TestCase):

    def test_instantiate(self):
        job_repository = FakeJobRepository()
        self.assertIsNone(job_repository.get_jobs())
        self.assertIsNone(job_repository.get_job_by_status(None))
        self.assertIsNone(job_repository.get_jobs_by_status(None))
        self.assertIsNone(job_repository.exists_jobs_with_status(None))
        self.assertIsNone(job_repository.add_job(None))
        self.assertIsNone(job_repository.update_job(None))
        self.assertIsNone(job_repository.update_jobs(None))
        self.assertIsNone(job_repository.try_set_lock_on_job(None))


class FakeJobRepository(AbstractJobRepository):

    def get_jobs(self):
        return AbstractJobRepository.get_jobs(self)

    def get_job_by_status(self, status):
        return AbstractJobRepository.get_job_by_status(self, status)

    def get_jobs_by_status(self, status):
        return AbstractJobRepository.get_jobs_by_status(self, status)

    def exists_jobs_with_status(self, status):
        return AbstractJobRepository.exists_jobs_with_status(self, status)

    def add_job(self, job):
        return AbstractJobRepository.add_job(self, job)

    def update_job(self, job):
        return AbstractJobRepository.update_job(self, job)

    def update_jobs(self, jobs):
        return AbstractJobRepository.update_jobs(self, jobs)

    def try_set_lock_on_job(self, job):
        return AbstractJobRepository.try_set_lock_on_job(self, job)


if (__name__ == "__main__"):
    unittest.main()
