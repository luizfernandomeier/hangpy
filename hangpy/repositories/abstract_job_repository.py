from abc import ABC, abstractmethod
from hangpy.entities import Job
from hangpy.enums import JobStatus


class AbstractJobRepository(ABC):

    @abstractmethod
    def get_job_by_status(self, status: JobStatus) -> Job:
        pass

    @abstractmethod
    def get_jobs_by_status(self, status: JobStatus) -> list[Job]:
        pass

    @abstractmethod
    def exists_jobs_with_status(self, status: JobStatus) -> bool:
        pass

    @abstractmethod
    def add_job(self, job: Job):
        pass

    @abstractmethod
    def update_job(self, job: Job):
        pass

    @abstractmethod
    def update_jobs(self, jobs: list[Job]):
        pass

    @abstractmethod
    def try_set_lock_on_job(self, job: Job) -> bool:
        """The implementation of this method must be atomic"""
        pass
