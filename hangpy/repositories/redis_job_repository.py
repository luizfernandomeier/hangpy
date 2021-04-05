from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import AbstractJobRepository
from hangpy.services import JobActivityBase

class RedisJobRepository(AbstractJobRepository, RedisRepositoryBase):

    def __init__(self, redis_client):
        RedisRepositoryBase.__init__(self, redis_client)

    def get_jobs(self):
        keys = self._get_keys('job:*')
        serialized_jobs = self.redis_client.mget(keys)
        return self._deserialize_entries(serialized_jobs)
    
    def get_jobs_by_status(self, status: JobStatus):
        status_job_keys = self._get_keys(f'jobstatus:*:{str(status)}')
        job_keys = self.redis_client.mget(status_job_keys)
        serialized_jobs = self.redis_client.mget(job_keys)
        return self._deserialize_entries(serialized_jobs)

    def add_job(self, job_activity: JobActivityBase):
        job = job_activity.get_job_object()
        self.__set_job(job)

    def update_job(self, job: Job):
        self.__set_job(job)
    
    def update_jobs(self, jobs: list[Job]):
        for job in jobs:
            self.update_job(job)
    
    def try_set_lock_on_job(self, job: Job):
        return self.redis_client.setnx(f'lock:job:{job.id}', 1)

    def __set_job(self, job: Job):
        serialized_job = self._serialize_entry(job)
        self.__delete_job_status(job)
        self.redis_client.set(f'job:{job.id}', serialized_job)
        self.__set_job_status(job)

    def __delete_job_status(self, job: Job):
        keys = self._get_keys(f'jobstatus:{job.id}:*')
        for key in keys:
            self.redis_client.delete(key)

    def __set_job_status(self, job: Job):
        self.redis_client.set(f'jobstatus:{job.id}:{str(job.status)}', f'job:{job.id}')