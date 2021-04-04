import datetime
import threading
from abc import ABC, abstractmethod
from hangpy.entities import Job
from hangpy.enums import JobStatus

class JobActivityBase(ABC, threading.Thread):

    def __init__(self):
        self._started_to_run = False
        ABC.__init__(self)
        threading.Thread.__init__(self)

    @abstractmethod
    def action(self):
        pass

    def set_job(self, job: Job):
        self._job = job

    def get_job(self):
        return self._job

    def set_started_to_run(self):
        self._started_to_run = True
    
    def is_finished(self):
        return self._started_to_run and not self.is_alive()

    def set_job_status(self, status: JobStatus):
        self._job.status = status

    def set_job_error(self, err: Exception):
        self._job.error = str(err)
    
    def set_job_end_datetime(self):
        self._job.end_datetime = datetime.datetime.now().isoformat()

    def run(self):
        try:
            self.set_started_to_run()
            self.action()
            self.set_job_status(JobStatus.SUCCESS)
        except Exception as err:
            self.set_job_status(JobStatus.ERROR)
            self.set_job_error(err)
        self.set_job_end_datetime()
    
    def get_job_object(self):
        module_name = self.__module__
        class_name = self.__class__.__name__
        job = Job(module_name, class_name)
        return job