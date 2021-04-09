from hangpy.entities import Job
from hangpy.repositories import AbstractJobRepository


class JobService():
    """
    Provides an interface to add jobs to the queue.
    """

    def __init__(self,
                 job_repository: AbstractJobRepository):
        """
        Args:
            job_repository (AbstractJobRepository): Implementation of the job
            repository.
        """

        self.job_repository = job_repository

    def enqueue_job(self, job: Job):
        """
        Add job do the queue using the provided repository.

        Args:
            job (Job)
        """

        self.job_repository.add_job(job)
