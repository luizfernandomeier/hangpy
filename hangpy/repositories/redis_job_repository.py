from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.repositories import RedisRepositoryBase
from hangpy.repositories import JobRepository
from redis import Redis


class RedisJobRepository(JobRepository, RedisRepositoryBase):
    """Implementation of the JobRepository using Redis."""

    def __init__(self, redis_client: Redis):
        """
        Args:
            redis_client (Redis): Implementation of a Redis client.
        """
        RedisRepositoryBase.__init__(self, redis_client)

    def get_jobs(self) -> list[Job]:
        keys = self._get_keys('job:*')
        serialized_jobs = self.redis_client.mget(keys)
        return self._deserialize_entries(serialized_jobs)

    def get_job_by_status(self, status: JobStatus) -> Job:
        status_job_key = self._get_key(f'jobstatus:*:{str(status)}')
        if (status_job_key is None):
            return None
        job_key = self.redis_client.get(status_job_key)
        if (job_key is None):
            return None
        serialized_job = self.redis_client.get(job_key)
        return self._deserialize_entry(serialized_job)

    def __get_job_keys_by_status(self, status: JobStatus) -> list[str]:
        """Internal function for returning the Redis keys for jobs filtered by
        status.

        Args:
            status (JobStatus)

        Returns:
            list[str]
        """
        return self._get_keys(f'jobstatus:*:{str(status)}')

    def get_jobs_by_status(self, status: JobStatus) -> list[Job]:
        status_job_keys = self.__get_job_keys_by_status(status)
        job_keys = self.redis_client.mget(status_job_keys)
        serialized_jobs = self.redis_client.mget(job_keys)
        return self._deserialize_entries(serialized_jobs)

    def exists_jobs_with_status(self, status: JobStatus) -> bool:
        status_job_keys = self.__get_job_keys_by_status(status)
        return len(status_job_keys) > 0

    def add_job(self, job: Job):
        self.__set_job(job)

    def update_job(self, job: Job):
        self.__set_job(job)

    def update_jobs(self, jobs: list[Job]):
        for job in jobs:
            self.update_job(job)

    def try_set_lock_on_job(self, job: Job) -> bool:
        return bool(self.redis_client.setnx(f'lock:job:{job.id}', 1))

    def __set_job(self, job: Job):
        """Internal function to unify the command 'set' used for both add and
        update instructions on Redis. It also mantains a secondary index for
        jobs on the database to make possible to apply a filter by job status.

        Args:
            job (Job)
        """

        serialized_job = self._serialize_entry(job)
        self.__delete_job_status(job)
        self.redis_client.set(f'job:{job.id}', serialized_job)
        self.__set_job_status(job)

    def __delete_job_status(self, job: Job):
        """Internal function to delete the secondary index by status kept on
        Redis.

        Args:
            job (Job)
        """

        keys = self._get_keys(f'jobstatus:{job.id}:*')
        for key in keys:
            self.redis_client.delete(key)

    def __set_job_status(self, job: Job):
        """Internal function to set the secondary index by status kept on
        Redis.

        Args:
            job (Job)
        """

        self.redis_client.set(f'jobstatus:{job.id}:{str(job.status)}', f'job:{job.id}')
