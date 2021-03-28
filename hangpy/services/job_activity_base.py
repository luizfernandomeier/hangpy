import inspect
from hangpy.entities import Job

class JobActivityBase():

    def action(self):
        pass

    def start(self):
        self.action()
    
    def get_job_object(self):
        module_name = self.__get_module_name()
        class_name = self.__class__.__name__
        job = Job(module_name, class_name)
        return job

    def __get_module_name(self):
        module_name = self.__module__
        if ('__main__' in module_name):
            module_name = self.__get_module_name_as_main()
        return module_name

    def __get_module_name_as_main(self):
        module_object = inspect.getmodule(self)
        module_name = inspect.getmodulename(module_object.__file__)
        if (module_object.__package__ == ''):
            return module_name
        return f'{mod_obj.__package__}.{module_name}'