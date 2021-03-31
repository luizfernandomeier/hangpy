from abc import ABC, abstractmethod
from hangpy.entities import Job

class JobActivityBase(ABC):

    @abstractmethod
    def action(self):
        pass

    def start(self):
        self.action()
    
    def get_job_object(self):
        module_name = self.__module__
        class_name = self.__class__.__name__
        job = Job(module_name, class_name)
        return job