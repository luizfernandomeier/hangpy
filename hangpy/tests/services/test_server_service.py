import datetime
from freezegun import freeze_time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities import Job
from hangpy.entities import Server
from hangpy.enums import JobStatus
from hangpy.services import ServerService
from unittest import TestCase, mock, main

class FakeJobRepository:
    def get_jobs_by_status(self, status):
        job = Job('module_test', 'class_test')
        return [job, job, job]
    
    def update_job(self, job):
        global fake_job_repository_update_job_run_count
        fake_job_repository_update_job_run_count += 1
    
    def update_jobs(self, jobs):
        global fake_job_repository_update_jobs_run_count
        global fake_job_repository_update_jobs_test_count
        fake_job_repository_update_jobs_run_count += 1
        fake_job_repository_update_jobs_test_count += len(jobs)

class FakeServerRepository:
    def update_server(self, server):
        global fake_server_repository_update_server_run_count
        fake_server_repository_update_server_run_count += 1

class FakeJobActivity:

    def __init__(self):
        self.finished = False

    def start(self):
        global fake_job_activity_start_run_count
        fake_job_activity_start_run_count += 1
    
    def is_finished(self):
        return self.finished

class FakeJobActivityException:
    def start(self):
        global fake_job_activity_exception_start_run_count
        fake_job_activity_exception_start_run_count += 1
        raise Exception('FakeJobActivityException exception')

def run_enabled_side_effect(*args):
    global run_enabled_run_count
    run_enabled_run_count += 1
    return (run_enabled_run_count <= 2)

def run_cycle_side_effect(*args):
    global run_cycle_run_count
    run_cycle_run_count += 1

def get_enqueued_jobs_side_effect(*args):
    job = Job('module_test', 'class_test')
    return [job, job, job]

def run_job_side_effect(*args):
    global run_job_run_count
    run_job_run_count += 1

def run_job_exception_side_effect(*args):
    raise Exception('run_job_exception_side_effect exception')

def log_side_effect(*args):
    global log_exception_message_test
    log_exception_message_test = args[0]

def get_job_activity_instance_side_effect(*args):
    return FakeJobActivity()

def get_job_activity_instance_exception_side_effect(*args):
    return FakeJobActivityException()

def clear_finished_jobs_side_effect(*args):
    global clear_finished_jobs_run_count
    clear_finished_jobs_run_count += 1

def slots_limit_reached_side_effect(*args):
    global slots_limit_reached_run_count
    slots_limit_reached_run_count += 1
    return (slots_limit_reached_run_count <= 1)

def save_finished_jobs_side_effect(*args):
    global save_finished_jobs_run_count
    save_finished_jobs_run_count += 1

def remove_finished_jobs_side_effect(*args):
    global remove_finished_jobs_run_count
    remove_finished_jobs_run_count += 1

def print_side_effect(*args):
    global print_message_test
    print_message_test = args[0]

class TestServerService(TestCase):

    def setUp(self):
        global run_enabled_run_count
        global run_cycle_run_count
        global run_job_run_count
        global log_exception_message_test
        global fake_job_activity_start_run_count
        global fake_job_activity_exception_start_run_count
        global fake_server_repository_update_server_run_count
        global fake_job_repository_update_job_run_count
        global fake_job_repository_update_jobs_run_count
        global fake_job_repository_update_jobs_test_count
        global print_message_test
        global clear_finished_jobs_run_count
        global slots_limit_reached_run_count
        global save_finished_jobs_run_count
        global remove_finished_jobs_run_count
        global updated_jobs_run_count
        run_enabled_run_count = 0
        run_cycle_run_count = 0
        run_job_run_count = 0
        log_exception_message_test = None
        fake_job_activity_start_run_count = 0
        fake_job_activity_exception_start_run_count = 0
        fake_server_repository_update_server_run_count = 0
        fake_job_repository_update_job_run_count = 0
        fake_job_repository_update_jobs_run_count = 0
        fake_job_repository_update_jobs_test_count = 0
        print_message_test = None
        clear_finished_jobs_run_count = 0
        slots_limit_reached_run_count = 0
        save_finished_jobs_run_count = 0
        remove_finished_jobs_run_count = 0
        updated_jobs_run_count = 0

    def tearDownClass():
        global run_enabled_run_count
        global run_cycle_run_count
        global run_job_run_count
        global log_exception_message_test
        global fake_job_activity_start_run_count
        global fake_job_activity_exception_start_run_count
        global fake_server_repository_update_server_run_count
        global fake_job_repository_update_job_run_count
        global fake_job_repository_update_jobs_run_count
        global fake_job_repository_update_jobs_test_count
        global print_message_test
        global clear_finished_jobs_run_count
        global slots_limit_reached_run_count
        global save_finished_jobs_run_count
        global remove_finished_jobs_run_count
        global updated_jobs_run_count
        del(run_enabled_run_count)
        del(run_cycle_run_count)
        del(run_job_run_count)
        del(log_exception_message_test)
        del(fake_job_activity_start_run_count)
        del(fake_job_activity_exception_start_run_count)
        del(fake_server_repository_update_server_run_count)
        del(fake_job_repository_update_job_run_count)
        del(fake_job_repository_update_jobs_run_count)
        del(fake_job_repository_update_jobs_test_count)
        del(print_message_test)
        del(clear_finished_jobs_run_count)
        del(slots_limit_reached_run_count)
        del(save_finished_jobs_run_count)
        del(remove_finished_jobs_run_count)
        del(updated_jobs_run_count)

    @mock.patch('hangpy.services.server_service.ServerService.run_enabled', side_effect=run_enabled_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.run_cycle', side_effect=run_cycle_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.sleep_cycle')
    @mock.patch('hangpy.services.server_service.ServerService.set_server_stop_state')
    def test_run(self, run_enabled_mock, run_cycle_mock, sleep_cycle_mock, set_server_stop_state_mock):
        global run_cycle_run_count
        server_service = ServerService(None, None, None, None)
        server_service.run()
        self.assertEqual(run_cycle_run_count, 2)

    def test_sleep_cycle(self):
        server_configuration = ServerConfigurationDto(1000)
        server_service = ServerService(None, server_configuration, None, None)
        time_start = datetime.datetime.now()
        server_service.sleep_cycle()
        time_stop = datetime.datetime.now()
        total_milliseconds = (time_stop - time_start).seconds * 1000
        total_milliseconds += (time_stop - time_start).microseconds / 1000
        self.assertGreater(total_milliseconds, 1000)

    def test_run_enabled(self):
        server_service = ServerService(None, None, None, None)
        server_service.stop_signal = False
        self.assertTrue(server_service.run_enabled())
        server_service.stop_signal = True
        self.assertFalse(server_service.run_enabled())
    
    @mock.patch('hangpy.services.server_service.ServerService.set_server_cycle_state')
    @mock.patch('hangpy.services.server_service.ServerService.clear_finished_jobs')
    @mock.patch('hangpy.services.server_service.ServerService.get_enqueued_jobs', side_effect=get_enqueued_jobs_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.run_enabled', side_effect=run_enabled_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.wait_until_slot_is_open')
    @mock.patch('hangpy.services.server_service.ServerService.run_job', side_effect=run_job_side_effect)
    def test_run_cycle(self, set_server_cycle_state_mock, clear_finished_jobs_mock, get_enqueued_jobs_mock, run_enabled_mock, wait_until_slot_is_open_mock, run_job_mock):
        global run_job_run_count
        server_service = ServerService(None, None, None, None)
        server_service.run_cycle()
        self.assertEqual(run_job_run_count, 2)

    @mock.patch('hangpy.services.server_service.ServerService.set_server_cycle_state')
    @mock.patch('hangpy.services.server_service.ServerService.clear_finished_jobs')
    @mock.patch('hangpy.services.server_service.ServerService.get_enqueued_jobs', side_effect=get_enqueued_jobs_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.run_enabled', return_value=True)
    @mock.patch('hangpy.services.server_service.ServerService.wait_until_slot_is_open')
    @mock.patch('hangpy.services.server_service.ServerService.run_job', side_effect=run_job_exception_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.log', side_effect=log_side_effect)
    def test_run_cycle_exception(self, set_server_cycle_state_mock, clear_finished_jobs_mock, get_enqueued_jobs_mock, run_enabled_mock, wait_until_slot_is_open_mock, run_job_mock, log_mock):
        global log_exception_message_test
        server_service = ServerService(None, None, None, None)
        server_service.run_cycle()
        self.assertTrue(log_exception_message_test.endswith('run_job_exception_side_effect exception'))
    
    @mock.patch('hangpy.services.server_service.ServerService.slots_limit_reached', side_effect=slots_limit_reached_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.clear_finished_jobs', side_effect=clear_finished_jobs_side_effect)
    def test_wait_until_slot_is_open(self, slots_limit_reached_mock, clear_finished_jobs_mock):
        global clear_finished_jobs_run_count
        global slots_limit_reached_run_count
        server_service = ServerService(None, None, None, None)
        server_service.wait_until_slot_is_open()
        self.assertEqual(clear_finished_jobs_run_count, 1)
        self.assertEqual(slots_limit_reached_run_count, 2)
    
    def test_slots_limit_reached(self):
        server = Server(2)
        server_service = ServerService(server, None, None, None)
        job_activity = FakeJobActivity()
        server_service.job_activities_assigned.append(job_activity)
        self.assertFalse(server_service.slots_limit_reached())

        server_service.job_activities_assigned.append(job_activity)
        self.assertTrue(server_service.slots_limit_reached())

        server_service.job_activities_assigned.append(job_activity)
        self.assertTrue(server_service.slots_limit_reached())

        server_service.job_activities_assigned.clear()
        self.assertFalse(server_service.slots_limit_reached())

    @mock.patch('hangpy.services.server_service.ServerService.save_finished_jobs', side_effect=save_finished_jobs_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.remove_finished_jobs', side_effect=remove_finished_jobs_side_effect)
    def test_clear_finished_jobs(self, save_finished_jobs_mock, remove_finished_jobs_mock):
        global save_finished_jobs_run_count
        global remove_finished_jobs_run_count
        server_service = ServerService(None, None, None, None)
        server_service.clear_finished_jobs()
        self.assertEqual(save_finished_jobs_run_count, 1)
        self.assertEqual(remove_finished_jobs_run_count, 1)
    
    def test_save_finished_jobs(self):
        global fake_job_repository_update_jobs_run_count
        server_service = ServerService(None, None, None, FakeJobRepository())
        job_activity_running = FakeJobActivity()
        server_service.job_activities_assigned.append(job_activity_running)
        server_service.save_finished_jobs()
        self.assertEqual(fake_job_repository_update_jobs_run_count, 1)
        self.assertEqual(fake_job_repository_update_jobs_test_count, 0)

        job_activity_finished = FakeJobActivity()
        job_activity_finished.finished = True
        server_service.job_activities_assigned.append(job_activity_finished)
        server_service.save_finished_jobs()
        self.assertEqual(fake_job_repository_update_jobs_run_count, 2)
        self.assertEqual(fake_job_repository_update_jobs_test_count, 1)
    
    def test_remove_finished_jobs(self):
        server_service = ServerService(None, None, None, None)
        job_activity_running = FakeJobActivity()
        server_service.job_activities_assigned.append(job_activity_running)
        server_service.remove_finished_jobs()
        self.assertEqual(len(server_service.job_activities_assigned), 1)

        job_activity_finished = FakeJobActivity()
        job_activity_finished.finished = True
        server_service.job_activities_assigned.append(job_activity_finished)
        server_service.remove_finished_jobs()
        self.assertEqual(len(server_service.job_activities_assigned), 1)

    def test_get_enqueued_jobs(self):
        server_service = ServerService(None, None, None, FakeJobRepository())
        enqueued_jobs = server_service.get_enqueued_jobs()
        self.assertEqual(len(enqueued_jobs), 3)

    @mock.patch('hangpy.services.server_service.ServerService.set_job_start_state')
    @mock.patch('hangpy.services.server_service.ServerService.get_job_activity_instance', side_effect=get_job_activity_instance_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.add_job_activity_assigned')
    @mock.patch('hangpy.services.server_service.ServerService.log')
    def test_run_job(self, set_job_start_state_mock, get_job_activity_instance_mock, add_job_activity_assigned_mock, log_mock):
        server_service = ServerService(None, None, None, None)
        job = Job('module_test', 'class_test')
        server_service.run_job(job)
        self.assertEqual(fake_job_activity_start_run_count, 1)

    @mock.patch('hangpy.services.server_service.ServerService.set_job_start_state')
    @mock.patch('hangpy.services.server_service.ServerService.get_job_activity_instance', side_effect=get_job_activity_instance_exception_side_effect)
    @mock.patch('hangpy.services.server_service.ServerService.add_job_activity_assigned')
    @mock.patch('hangpy.services.server_service.ServerService.log', side_effect=log_side_effect)
    def test_run_job_exception(self, set_job_start_state_mock, get_job_activity_instance_mock, add_job_activity_assigned_mock, log_mock):
        server_service = ServerService(None, None, None, None)
        job = Job('module_test', 'class_test')
        server_service.run_job(job)
        self.assertEqual(fake_job_activity_exception_start_run_count, 1)
        self.assertTrue(log_exception_message_test.endswith('FakeJobActivityException exception'))

    def test_add_job_activity_assigned(self):
        server_service = ServerService(None, None, None, None)
        job_activity = FakeJobActivity()
        server_service.add_job_activity_assigned(job_activity)
        self.assertEqual(len(server_service.job_activities_assigned), 1)
        
        server_service.add_job_activity_assigned(job_activity)
        self.assertEqual(len(server_service.job_activities_assigned), 2)

    def test_get_job_activity_instance(self):
        server_service = ServerService(None, None, None, None)
        job = Job(FakeJobActivity().__module__, FakeJobActivity().__class__.__name__)
        job_instance = server_service.get_job_activity_instance(job)
        self.assertIsInstance(job_instance, FakeJobActivity)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_server_cycle_state(self):
        global fake_server_repository_update_server_run_count
        server = Server()
        server_service = ServerService(server, None, FakeServerRepository(), None)
        server_service.set_server_cycle_state()
        self.assertEqual(server.last_cycle_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(fake_server_repository_update_server_run_count, 1)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_server_stop_state(self):
        global fake_server_repository_update_server_run_count
        server = Server()
        server_service = ServerService(server, None, FakeServerRepository(), None)
        server_service.set_server_stop_state()
        self.assertEqual(server.stop_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(fake_server_repository_update_server_run_count, 1)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_job_start_state(self):
        global fake_job_repository_update_job_run_count
        job = Job('module_test', 'class_test')
        server_service = ServerService(None, None, None, FakeJobRepository())
        server_service.set_job_start_state(job)
        self.assertEqual(job.start_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(job.status, JobStatus.PROCESSING)
        self.assertEqual(fake_job_repository_update_job_run_count, 1)
    
    @mock.patch('builtins.print', side_effect=print_side_effect)
    def test_log(self, print_mock):
        global print_message_test
        server_service = ServerService(None, None, None, None)
        server_service.log('some log message')
        self.assertEqual(print_message_test, 'some log message')

if (__name__ == "__main__"):
    main()