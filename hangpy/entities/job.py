import datetime
import uuid
from hangpy.enums import JobStatus


class Job():
    """Represents a set of instructions to instantiate and execute an action
    defined by a class that inherits from JobActivityBase.
    """

    def __init__(self, module_name: str, class_name: str, parameters: list = None):
        """
        Args:
            module_name (str): Full module name of the class that contains
            the action to be executed.
            class_name (str): Name of the class that contains the action to
            be executed.
            parameters (list, optional): List of parameters that will be
            passed to the action to be executed. Defaults to None.
        """

        self.__validate_parameters(module_name, class_name, parameters)
        self.id = str(uuid.uuid4())
        self.module_name = module_name
        self.class_name = class_name
        self.status = JobStatus.ENQUEUED
        self.error = None
        self.enqueued_datetime = datetime.datetime.now().isoformat()
        self.start_datetime = None
        self.end_datetime = None
        self.parameters = []
        if (parameters is not None):
            self.parameters.extend(parameters)

    def __validate_parameters(self, module_name: str, class_name: str, parameters: list):
        """Internal function used to validate the class constructor parameters."""

        self.__validate_module_name(module_name)
        self.__validate_class_name(class_name)
        self.__validate_parameters_argument(parameters)

    def __validate_module_name(self, module_name: str):
        """
        Internal function used to validate the 'module_name' value.

        Raises:
            ValueError: The value must be a string
            ValueError: The value must not be empty
        """

        if (not isinstance(module_name, str)):
            raise ValueError('module_name', module_name, 'The value must be a string')
        if (not module_name):
            raise ValueError('module_name', module_name, 'The value must not be empty')

    def __validate_class_name(self, class_name: str):
        """
        Internal function used to validate the 'class_name' value.

        Raises:
            ValueError: The value must be a string
            ValueError: The value must not be empty
        """

        if (not isinstance(class_name, str)):
            raise ValueError('class_name', class_name, 'The value must be a string')
        if (not class_name):
            raise ValueError('class_name', class_name, 'The value must not be empty')

    def __validate_parameters_argument(self, parameters: list):
        """
        Internal function used to validate the 'parameters' value.

        Raises:
            ValueError: The value must be a list or None
        """

        if (not isinstance(parameters, list) and parameters is not None):
            raise ValueError('parameters', parameters, 'The value must be a list or None')
