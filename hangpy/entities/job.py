import datetime
import uuid
from hangpy.enums import JobStatus

class Job():

    def __init__(self, module_name='', class_name='', parameters=None):
        self.id = str(uuid.uuid4())
        self.module_name = module_name
        self.class_name = class_name
        self.status = JobStatus.ENQUEUED
        self.enqueued_datetime = datetime.datetime.now().isoformat()
        self.start_datetime = None
        self.end_datetime = None
        self.parameters = []
        if (parameters is not None):
            self.parameters.extend(parameters)