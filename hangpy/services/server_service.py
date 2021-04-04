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
        self.job_activities_assigned = []
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
            self.clear_finished_jobs()
            jobs = self.get_enqueued_jobs()
            for job in jobs:
                if (not self.run_enabled()):
                    break
                self.wait_until_slot_is_open()
                self.run_job(job)
        except Exception as err:
            self.log(f'An error ocurred during the job processing cycle: {err}')

    def wait_until_slot_is_open(self):
        while (self.slots_limit_reached()):
            self.clear_finished_jobs()
            time.sleep(0.1)
    
    def slots_limit_reached(self):
        return len(self.job_activities_assigned) >= self.server.slots

    def clear_finished_jobs(self):
        self.save_finished_jobs()
        self.remove_finished_jobs()        

    def save_finished_jobs(self):
        finished_jobs = [job_activity.get_job() for job_activity in self.job_activities_assigned if job_activity.is_finished()]
        self.job_repository.update_jobs(finished_jobs)

    def remove_finished_jobs(self):
        self.job_activities_assigned = [job_activity for job_activity in self.job_activities_assigned if not job_activity.is_finished()]

    def get_enqueued_jobs(self):
        return self.job_repository.get_jobs_by_status(JobStatus.ENQUEUED)

    def run_job(self, job):
        try:
            self.set_job_start_state(job)
            self.log(f'\nProcessing job: {job.id}')
            job_activity_instance = self.get_job_activity_instance(job)
            self.add_job_activity_assigned(job_activity_instance)
            job_activity_instance.start()
        except Exception as err:
            self.log(f'Error: {err}')

    def add_job_activity_assigned(self, job_activity_instance):
        self.job_activities_assigned.append(job_activity_instance)

    def get_job_activity_instance(self, job):
        job_module = importlib.import_module(job.module_name)
        job_class = getattr(job_module, job.class_name)
        job_activity_instance = job_class()
        job_activity_instance.set_job(job)
        return job_activity_instance

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
    
    # TODO: Implement custom logger
    def log(self, message):
        print(message)