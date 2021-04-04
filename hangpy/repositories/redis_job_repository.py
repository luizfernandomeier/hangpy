from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import AbstractJobRepository
from hangpy.services import JobActivityBase

class RedisJobRepository(AbstractJobRepository, RedisRepositoryBase):

    def __init__(self, redis_client):
        RedisRepositoryBase.__init__(self, redis_client)

    def get_jobs(self):
        keys = self._get_keys('job.*')
        serialized_jobs = self.redis_client.mget(keys)
        return self._deserialize_entries(serialized_jobs)
    
    # TODO: refactor this method so it doesn't need to get all the jobs each time
    def get_jobs_by_status(self, status: JobStatus):
        jobs = self.get_jobs()
        return [job for job in jobs if job.status is status]

    def add_job(self, job_activity: JobActivityBase):
        job = job_activity.get_job_object()
        self.__set_job(job)

    def update_job(self, job: Job):
        self.__set_job(job)
    
    def update_jobs(self, jobs: list[Job]):
        for job in jobs:
            self.update_job(job)
    
    def try_set_lock_on_job(self, job: Job):
        return self.redis_client.setnx(f'lock.job.{job.id}', 1)

    def __set_job(self, job: Job):
        serialized_job = self._serialize_entry(job)
        self.redis_client.set(f'job.{job.id}', serialized_job)