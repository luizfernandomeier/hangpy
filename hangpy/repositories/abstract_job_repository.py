from abc import ABC, abstractmethod

class AbstractJobRepository(ABC):

    @abstractmethod
    def get_jobs(self):
        pass

    @abstractmethod
    def get_jobs_by_status(self, status):
        pass

    @abstractmethod
    def add_job(self, job):
        pass

    @abstractmethod
    def update_job(self, job):
        pass

    @abstractmethod
    def update_jobs(self, jobs):
        pass

    @abstractmethod
    def try_set_lock_on_job(self, job):
        """The implementation of this method must be atomic"""
        pass