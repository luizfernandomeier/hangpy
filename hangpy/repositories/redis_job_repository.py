import jsonpickle
import redis
from hangpy.enums import JobStatus
from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import AbstractJobRepository

class RedisJobRepository(AbstractJobRepository, RedisRepositoryBase):

    def __init__(self, host, port, password=None):
        RedisRepositoryBase.__init__(self, host, port, password)

    def get_jobs(self):
        keys = self._get_keys('job.*')
        serialized_jobs = self.client.mget(keys)
        return self._deserialize_entries(serialized_jobs)
    
    # TODO: refactor this method so it doesn't need to get all the jobs each time
    def get_jobs_by_status(self, status):
        jobs = self.get_jobs()
        return [job for job in jobs if job.status is status]

    def add_job(self, job_activity):
        job = job_activity.get_job_object()
        self.__set_job(job)

    def update_job(self, job):
        self.__set_job(job)

    def __set_job(self, job):
        serialized_job = jsonpickle.encode(job)
        self.client.set(f'job.{job.id}', serialized_job)