import datetime
import importlib
import threading
import time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities import Job, Server
from hangpy.enums import JobStatus
from hangpy.repositories import JobRepository, ServerRepository
from hangpy.services import JobActivityBase, LogService


class ServerService(threading.Thread):
    """
    Manages the execution of the job queue.
    Use this class when implementing a HangPy server.
    """

    def __init__(self,
                 server_configuration: ServerConfigurationDto,
                 server_repository: ServerRepository,
                 job_repository: JobRepository,
                 log_service: LogService = None):
        """
        Args:
            server_configuration (ServerConfigurationDto): Class contaning the
            configuration to be used by this server instance.
            server_repository (ServerRepository): Implementation of
            the server repository.
            job_repository (JobRepository): Implementation of the job
            repository.
            log_service (LogService): Logger.
        """

        self.stop_signal = False
        self.server = Server(server_configuration)
        self.server_repository = server_repository
        self.job_repository = job_repository
        self.log_service = log_service
        self.job_activities_assigned = []
        threading.Thread.__init__(self)

    def run(self):
        """
        Controls the flow of the execution cycles of the server instance.

        To start the server, use the function 'start'.
        """

        self.set_server_start_state()
        self.log_run()
        while (self.run_enabled()):
            self.try_run_cycle()
            self.sleep_cycle()
        self.wait_until_slots_are_empty()
        self.set_server_stop_state()

    def log_run(self):
        message = ('The HangPy server is running!'
                   f'\nServer id: {self.server.id}'
                   f'\nStarted: {self.server.start_datetime}'
                   f'\nInterval: {self.server.configuration.cycle_interval_milliseconds} ms'
                   f'\nSlots: {self.server.configuration.slots}')
        self.log(message)

    def sleep_cycle(self):
        """
        Waits the time configured for the server instance in between cycles.
        """

        time.sleep(self.server.configuration.cycle_interval_milliseconds / 1000)

    def run_enabled(self) -> bool:
        """
        Returns 'False' if the stop signal has been set.
        In this case, the server will prepare for shutdown.

        Returns:
            bool
        """

        return not self.stop_signal

    def try_run_cycle(self):
        """
        Try to run the cycle actions, catching and logging any eventual
        exceptions.
        """

        try:
            self.run_cycle()
        except Exception as err:
            self.log(f'An error ocurred during the job processing cycle: {err}')

    def run_cycle(self):
        """
        Keeps the cycle running as long as necessary.
        """

        self.set_server_cycle_state()
        while (self.must_run_cycle_loop()):
            self.run_cycle_loop()

    def run_cycle_loop(self):
        """
        Function responsible for trying to get, lock and run the next enqueued
        job.
        """

        self.clear_finished_jobs()
        self.wait_until_slot_is_open()
        job = self.get_next_enqueued_job()
        if (job is None):
            time.sleep(0.1)
            return
        if (self.try_set_lock_on_job(job)):
            self.run_job(job)

    def must_run_cycle_loop(self) -> bool:
        """
        Returns 'True' if the cycle must continue running and 'False' if the
        server instance can go idle until the next cycle.

        Returns:
            bool
        """

        run_necessity = self.exists_enqueued_jobs() or not self.slots_empty()
        return self.run_enabled() and run_necessity

    def wait_until_slot_is_open(self):
        """
        Keep the server instance waiting until a slot in open for running the
        next enqueued job.
        """

        while (self.slots_limit_reached()):
            self.clear_finished_jobs()
            time.sleep(0.1)

    def wait_until_slots_are_empty(self):
        """
        Keep the server instance waiting while there are any jobs running.
        """

        while (not self.slots_empty()):
            self.clear_finished_jobs()
            time.sleep(0.1)

    def slots_limit_reached(self) -> bool:
        """
        Returns 'True' if all slots available for this server instance are
        currently in use, and 'False' if there is any slots available.

        Returns:
            bool
        """

        return len(self.job_activities_assigned) >= self.server.configuration.slots

    def slots_empty(self) -> bool:
        """
        Returns 'True' if none of the slots are currently in use for
        processing jobs.

        Returns:
            bool
        """

        return len(self.job_activities_assigned) == 0

    def clear_finished_jobs(self):
        """
        Tries to save the any finished jobs on this server instance to the
        repository, and stop tracking them on the instance's list.
        """

        self.save_finished_jobs()
        self.untrack_jobs()

    def save_finished_jobs(self):
        """
        Find all the finished jobs on this server instance, saves them on the
        repository, and mark them to be untracked.
        """

        finished_activities = [job_activity for job_activity in self.job_activities_assigned if job_activity.is_finished()]
        finished_jobs = [job_activity.get_job() for job_activity in finished_activities]
        self.job_repository.update_jobs(finished_jobs)
        for job_activity in finished_activities:
            job_activity.set_can_be_untracked()

    def untrack_jobs(self):
        """
        Find all the jobs marked to be untracked and remove them from the
        server instance memory list.
        """

        self.job_activities_assigned = [job_activity for job_activity in self.job_activities_assigned
                                        if not job_activity.can_be_untracked()]

    def exists_enqueued_jobs(self) -> bool:
        """
        Returns 'True' if there is at least one enqueued job in the
        repository, and returns 'False' if there is none.

        Returns:
            bool
        """

        return self.job_repository.exists_jobs_with_status(JobStatus.ENQUEUED)

    def get_next_enqueued_job(self) -> Job:
        """
        Get a enqueued job from the repository. If there is none, returns
        'None'.

        Returns:
            Job
        """

        return self.job_repository.get_job_by_status(JobStatus.ENQUEUED)

    def run_job(self, job: Job):
        """
        Manages the execution of the actions defined on the activity class.

        Args:
            job (Job)
        """
        try:
            self.set_job_start_state(job)
            self.log(f'\nProcessing job: {job.id}')
            job_activity_instance = self.get_job_activity_instance(job)
            self.add_job_activity_assigned(job_activity_instance)
            self.run_job_instance(job_activity_instance)
        except Exception as err:
            self.log(f'Error: {err}')

    def run_job_instance(self, job_activity_instance: JobActivityBase):
        """
        Starts a thread to process the activity instance.

        Args:
            job_activity_instance (JobActivityBase)
        """

        job_activity_instance.start()

    def add_job_activity_assigned(self, job_activity_instance: JobActivityBase):
        """
        Tracks the activity instance of the server instance memory list.

        Args:
            job_activity_instance (JobActivityBase)
        """

        self.job_activities_assigned.append(job_activity_instance)

    def get_job_activity_instance(self, job: Job) -> JobActivityBase:
        """
        Returns an instance of the class defined by the job, that inherits
        from 'JobActivityBase'. Is also fills the job entity relationship
        on this instance.

        Args:
            job (Job)

        Returns:
            JobActivityBase
        """

        job_module = importlib.import_module(job.module_name)
        job_class = getattr(job_module, job.class_name)
        job_activity_instance = job_class()
        job_activity_instance.set_job(job)
        return job_activity_instance

    def set_server_start_state(self):
        """
        Fill the properties necessary when the server instance starts.
        """

        self.server.start_datetime = datetime.datetime.now().isoformat()
        self.server_repository.add_server(self.server)

    def set_server_cycle_state(self):
        """
        Fill the properties necessary when the server instance cycle runs.
        """

        self.server.last_cycle_datetime = datetime.datetime.now().isoformat()
        self.server_repository.update_server(self.server)

    def set_server_stop_state(self):
        """
        Fill the properties necessary when the server instance stops.
        """

        self.server.stop_datetime = datetime.datetime.now().isoformat()
        self.server_repository.update_server(self.server)

    def set_job_start_state(self, job: Job):
        """
        Fill the properties necessary when the job starts.
        """

        job.start_datetime = datetime.datetime.now().isoformat()
        job.status = JobStatus.PROCESSING
        self.job_repository.update_job(job)

    def try_set_lock_on_job(self, job: Job) -> bool:
        """
        Locks the job on the repository, informing all servers that it is
        currently being handled by this server. Returns 'True' if the server
        could obtain the lock and 'False' otherwise.

        Args:
            job (Job)

        Returns:
            bool
        """

        return self.job_repository.try_set_lock_on_job(job)

    def stop(self):
        """
        Send the stop signal to the server instance.
        """

        self.stop_signal = True
        self.log_stop()

    def log_stop(self):
        message = f'Server {self.server.id} shutdown in progress..'
        self.log(message)

    def join(self):
        threading.Thread.join(self)
        self.log_join()

    def log_join(self):
        message = f'Server {self.server.id} stopped.'
        self.log(message)

    def log(self, message: str):
        """
        Send the server log messages to the logger injected on this server
        instance.

        Args:
            message (str)
        """

        if (self.log_service is not None):
            self.log_service.log(message)
