from hangpy.repositories import JobRepository
from hangpy.services import JobActivityBase


class JobService():
    """
    Provides an interface to add jobs to the queue.
    """

    def __init__(self,
                 job_repository: JobRepository):
        """
        Args:
            job_repository (JobRepository): Implementation of the job
            repository.
        """

        self.job_repository = job_repository

    def enqueue_job(self, job_activity: JobActivityBase, parameters: list[str] = None):
        """
        Add job activity to the queue using the provided repository.

        Args:
            job (JobActivityBase)
            parameters (list[str])
        """

        job = job_activity.create_job_object(parameters)

        self.job_repository.add_job(job)
