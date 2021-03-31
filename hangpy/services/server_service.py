import datetime
import importlib
import threading
import time
from hangpy.enums import JobStatus

class ServerService(threading.Thread):
    
    def __init__(self, server, server_configuration, server_repository, job_repository):
        self.stop_signal = False
        self.server = server
        self.server_configuration = server_configuration
        self.server_repository = server_repository
        self.job_repository = job_repository
        threading.Thread.__init__(self)

    def run(self):
        while (self.run_enabled()):
            self.run_cycle()
            self.sleep_cycle()
        self.set_server_stop_state()

    def sleep_cycle(self):
        time.sleep(self.server_configuration.cycle_interval_milliseconds / 1000)
    
    def run_enabled(self):
        return not self.stop_signal
    
    def run_cycle(self):
        try:
            self.set_server_cycle_state()
            jobs = self.get_enqueued_jobs()
            for job in jobs:
                if (not self.run_enabled()):
                    break
                self.run_job(job)
        except Exception as err:
            self.log(f'An error ocurred during the job processing cycle: {err}')

    def get_enqueued_jobs(self):
        return self.job_repository.get_jobs_by_status(JobStatus.ENQUEUED)

    def run_job(self, job):
        self.set_job_start_state(job)
        try:
            self.log(f'\nProcessing job: {job.id}')
            job_activity_instance = self.get_job_activity_instance(job)
            job_activity_instance.start()
            job.status = JobStatus.SUCCESS
        except Exception as err:
            job.status = JobStatus.ERROR
            self.log(f'Error: {err}')
        self.set_job_stop_state(job)

    def get_job_activity_instance(self, job):
        job_module = importlib.import_module(job.module_name)
        job_class = getattr(job_module, job.class_name)
        return job_class()

    def set_server_cycle_state(self):
        self.server.last_cycle_datetime = datetime.datetime.now().isoformat()
        self.server_repository.update_server(self.server)

    def set_server_stop_state(self):
        self.server.stop_datetime = datetime.datetime.now().isoformat()
        self.server_repository.update_server(self.server)

    def set_job_start_state(self, job):
        job.start_datetime = datetime.datetime.now().isoformat()
        job.status = JobStatus.PROCESSING
        self.job_repository.update_job(job)

    def set_job_stop_state(self, job):
        job.end_datetime = datetime.datetime.now().isoformat()
        self.job_repository.update_job(job)
    
    # TODO: Implement custom logger
    def log(self, message):
        print(message)