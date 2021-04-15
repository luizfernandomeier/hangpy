from abc import ABC, abstractmethod
from hangpy.entities import Job
from hangpy.enums import JobStatus


class JobRepository(ABC):
    """
    Interface defining the functions necessary for a class to be used as job
    repository.
    """

    @abstractmethod
    def get_jobs(self) -> list[Job]:
        """
        Returns a list of all the job instances on the repository. If no jobs
        are found, and empty list is returned.

        Returns:
            list[Job]
        """
        pass

    @abstractmethod
    def get_job_by_status(self, status: JobStatus) -> Job:
        """
        Returns a single job instance that has the status passed by
        parameter. If no jobs are found, 'None' is returned.

        Args:
            status (JobStatus)

        Returns:
            Job
        """
        pass

    @abstractmethod
    def get_jobs_by_status(self, status: JobStatus) -> list[Job]:
        """
        Returns a list of job instances that have the status passed by
        parameter. If no jobs are found, and empty list is returned.

        Args:
            status (JobStatus)

        Returns:
            list[Job]
        """
        pass

    @abstractmethod
    def exists_jobs_with_status(self, status: JobStatus) -> bool:
        """
        Returns 'True' if a job with the status passed by parameter exists on
        the repository, and 'False' otherwise.

        Args:
            status (JobStatus)

        Returns:
            bool
        """
        pass

    @abstractmethod
    def add_job(self, job: Job):
        """
        Adds the job passed by parameter into the repository and commits the
        transaction.

        Args:
            job (Job)
        """
        pass

    @abstractmethod
    def update_job(self, job: Job):
        """
        Updates the job passed by parameter into the repository and commits
        the transaction.

        Args:
            job (Job)
        """
        pass

    @abstractmethod
    def update_jobs(self, jobs: list[Job]):
        """
        Updates the jobs passed by parameter into the repository and commits
        the transaction.

        Args:
            jobs (list[Job])
        """
        pass

    @abstractmethod
    def try_set_lock_on_job(self, job: Job) -> bool:
        """
        Locks the job on the repository, informing all servers that it is
        currently being handled by this server. This operation must be
        atomic. Returns 'True' if the server could obtain the lock and
        'False' otherwise.

        Args:
            job (Job)

        Returns:
            bool
        """
        pass
