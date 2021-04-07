import datetime
import importlib
import threading
import time
from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.services import JobActivityBase

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
            self.try_run_cycle()
            self.sleep_cycle()
        self.wait_until_slots_are_empty()
        self.set_server_stop_state()

    def sleep_cycle(self):
        time.sleep(self.server_configuration.cycle_interval_milliseconds / 1000)
    
    def run_enabled(self):
        return not self.stop_signal
    
    def try_run_cycle(self):
        try:
            self.run_cycle()
        except Exception as err:
            self.log(f'An error ocurred during the job processing cycle: {err}')

    def run_cycle(self):
        self.set_server_cycle_state()
        while (self.must_run_cycle_loop()):
            self.run_cycle_loop()

    def run_cycle_loop(self):
        self.clear_finished_jobs()
        self.wait_until_slot_is_open()
        job = self.get_next_enqueued_job()
        if (job is None):
            time.sleep(0.1)
            return
        if (self.try_set_lock_on_job(job)):
            self.run_job(job)
    
    def must_run_cycle_loop(self) -> bool:
        run_necessity = self.exists_enqueued_jobs() or not self.slots_empty()
        return self.run_enabled() and run_necessity

    def wait_until_slot_is_open(self):
        while (self.slots_limit_reached()):
            self.clear_finished_jobs()
            time.sleep(0.1)
    
    def wait_until_slots_are_empty(self):
        while (not self.slots_empty()):
            self.clear_finished_jobs()
            time.sleep(0.1)
    
    def slots_limit_reached(self):
        return len(self.job_activities_assigned) >= self.server.slots
    
    def slots_empty(self):
        return len(self.job_activities_assigned) == 0

    def clear_finished_jobs(self):
        self.save_finished_jobs()
        self.untrack_jobs()        

    def save_finished_jobs(self):
        finished_activities = [job_activity for job_activity in self.job_activities_assigned if job_activity.is_finished()]
        finished_jobs = [job_activity.get_job() for job_activity in finished_activities]
        self.job_repository.update_jobs(finished_jobs)
        for job_activity in finished_activities:
            job_activity.set_can_be_untracked()

    def untrack_jobs(self):
        self.job_activities_assigned = [job_activity for job_activity in self.job_activities_assigned if not job_activity.can_be_untracked()]

    def exists_enqueued_jobs(self):
        return self.job_repository.exists_jobs_with_status(JobStatus.ENQUEUED)

    def get_next_enqueued_job(self):
        return self.job_repository.get_job_by_status(JobStatus.ENQUEUED)

    def run_job(self, job: Job):
        try:
            self.set_job_start_state(job)
            self.log(f'\nProcessing job: {job.id}')
            job_activity_instance = self.get_job_activity_instance(job)
            self.add_job_activity_assigned(job_activity_instance)
            self.run_job_instance(job_activity_instance)
        except Exception as err:
            self.log(f'Error: {err}')

    def run_job_instance(self, job_activity_instance: JobActivityBase):
        job_activity_instance.start()

    def add_job_activity_assigned(self, job_activity_instance: JobActivityBase):
        self.job_activities_assigned.append(job_activity_instance)

    def get_job_activity_instance(self, job: Job):
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

    def set_job_start_state(self, job: Job):
        job.start_datetime = datetime.datetime.now().isoformat()
        job.status = JobStatus.PROCESSING
        self.job_repository.update_job(job)
    
    def try_set_lock_on_job(self, job: Job):
        return self.job_repository.try_set_lock_on_job(job)

    # TODO: Implement custom logger
    def log(self, message):
        print(message)