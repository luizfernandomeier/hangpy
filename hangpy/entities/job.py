import datetime
import uuid
from hangpy.enums import JobStatus

class Job():

    def __init__(self, module_name: str = '', class_name: str = '', parameters: list = None):
        self.__validate_parameters(module_name, class_name, parameters)
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

    def __validate_parameters(self, module_name, class_name, parameters):
        self.__validate_module_name(module_name)
        self.__validate_class_name(class_name)
        self.__validate_parameters_argument(parameters)

    def __validate_module_name(self, module_name):
        if (not isinstance(module_name, str)):
            raise ValueError('module_name', module_name, 'The value must be a string')
        if (not module_name):
            raise ValueError('module_name', module_name, 'The value must not be empty')

    def __validate_class_name(self, class_name):
        if (not isinstance(class_name, str)):
            raise ValueError('class_name', class_name, 'The value must be a string')
        if (not class_name):
            raise ValueError('class_name', class_name, 'The value must not be empty')

    def __validate_parameters_argument(self, parameters):
        if (not isinstance(parameters, list) and parameters is not None):
            raise ValueError('parameters', parameters, 'The value must be a list or None')