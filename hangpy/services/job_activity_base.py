import datetime
import threading
from abc import ABC, abstractmethod
from hangpy.entities import Job
from hangpy.enums import JobStatus


class JobActivityBase(ABC, threading.Thread):
    """
    Base class for any job activities intended to be processed using
    HangPy.
    """

    def __init__(self):
        self._started_to_run = False
        self._can_be_untracked = False
        ABC.__init__(self)
        threading.Thread.__init__(self)

    @abstractmethod
    def action(self):
        """
        Override this with a function containing the actions to be processed
        on the background job.
        """
        pass

    def set_job(self, job: Job):
        """
        Sets the property containing the entity that represents the job on the
        repository.

        Args:
            job (Job)
        """
        self._job = job

    def get_job(self) -> Job:
        """
        Gets the property containing the entity that represents the job on the
        repository.

        Returns:
            Job
        """
        return self._job

    def set_started_to_run(self):
        """Flags that activity started to run."""
        self._started_to_run = True

    def is_finished(self) -> bool:
        """
        Returns 'True' if the activity already ran and finished, and false
        if it didn't started to run or is running.

        Returns:
            bool
        """
        return self._started_to_run and not self.is_alive()

    def set_can_be_untracked(self):
        """
        Flags that this activity no longer need to be tracked by the server
        instance in memory.
        """
        self._can_be_untracked = True

    def can_be_untracked(self) -> bool:
        """
        Returns 'True' if the activity no longer need to be tracked by the
        server instance in memory.

        Returns:
            bool
        """
        return self._can_be_untracked

    def set_job_status(self, status: JobStatus):
        """
        Sets the status of the job entity that represents the activity.

        Args:
            status (JobStatus)
        """
        self._job.status = status

    def set_job_error(self, err: Exception):
        """
        Sets an error message on the job entity that represents the activity.

        Args:
            err (Exception)
        """
        self._job.error = str(err)

    def set_job_end_datetime(self):
        """
        Sets the current datetime as the end datetime of the job entity that
        represents the activity.
        """
        self._job.end_datetime = datetime.datetime.now().isoformat()

    def run(self):
        """
        Function used by the thread to run the action defined by the activity
        that inherits from this base class. It also provides the flow control
        of the execution and exception handling.

        To define the activity actions, override the 'action' function.
        """
        try:
            self.set_started_to_run()
            self.action()
            self.set_job_status(JobStatus.SUCCESS)
        except Exception as err:
            self.set_job_status(JobStatus.ERROR)
            self.set_job_error(err)
        self.set_job_end_datetime()

    def create_job_object(self, parameters: list[str] = None) -> Job:
        """
        Returns an instance of the entity that represents the job on the
        repository, based on the activity that inherits from this base class.

        Args:
            parameters (list[str])

        Returns:
            Job
        """
        module_name = self.__module__
        class_name = self.__class__.__name__
        job = Job(module_name, class_name)

        if (parameters is not None):
            job.parameters.extend(parameters)

        return job
