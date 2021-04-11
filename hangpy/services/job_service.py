from hangpy.repositories import AbstractJobRepository
from hangpy.services import JobActivityBase


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

    def enqueue_job(self, job_activity: JobActivityBase):
        """
        Add job activity to the queue using the provided repository.

        Args:
            job (JobActivityBase)
        """

        job = job_activity.create_job_object()
        self.job_repository.add_job(job)
