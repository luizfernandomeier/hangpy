import datetime
import types
from freezegun import freeze_time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities import Job, Server
from hangpy.enums import JobStatus
from hangpy.services import ServerService
from unittest import TestCase, mock, main

class FakeJobRepository:   
    def get_job_by_status(self, status):
        return get_fake_job()
    
    def update_job(self, job):
        global fake_job_repository_update_job_run_count
        fake_job_repository_update_job_run_count += 1
    
    def update_jobs(self, jobs):
        global fake_job_repository_update_jobs_run_count
        global fake_job_repository_update_jobs_test_count
        fake_job_repository_update_jobs_run_count += 1
        fake_job_repository_update_jobs_test_count += len(jobs)
    
    set_lock_return = True
    def try_set_lock_on_job(self, job):
        return self.set_lock_return

class FakeServerRepository:
    def update_server(self, server):
        global fake_server_repository_update_server_run_count
        fake_server_repository_update_server_run_count += 1

class FakeJobActivity:

    def __init__(self):
        self._finished = False
        self._can_be_untracked = False

    def start(self):
        global fake_job_activity_start_run_count
        fake_job_activity_start_run_count += 1
    
    def set_job(self, job):
        global fake_job_activity_set_job_run_count
        fake_job_activity_set_job_run_count += 1
    
    def get_job(self):
        return get_fake_job()
    
    def is_finished(self):
        return self._finished

    def set_can_be_untracked(self):
        global fake_job_activity_set_can_be_untracked_run_count
        fake_job_activity_set_can_be_untracked_run_count += 1
        self._can_be_untracked = True
    
    def can_be_untracked(self):
        return self._can_be_untracked

class FakeJobActivityException:
    def start(self):
        global fake_job_activity_exception_start_run_count
        fake_job_activity_exception_start_run_count += 1
        raise Exception('FakeJobActivityException exception')

def get_fully_qualified(method_mocked: str) -> str:
    return f'hangpy.services.server_service.ServerService.{method_mocked}'

def get_mock(method_mocked: str, args) -> mock.MagicMock:
    return next(mock for mock in args if f'name=\'{method_mocked}\'' in str(mock))

def get_call_count(method_mocked: str, args) -> int:
    return get_mock(method_mocked, args).call_count

def get_fake_job() -> Job:
    return Job('module_test', 'class_test')

def print_side_effect(*args):
    global print_message_test
    print_message_test = args[0]

class TestServerService(TestCase):

    def setUp(self):
        global fake_job_activity_start_run_count
        global fake_job_activity_set_job_run_count
        global fake_job_activity_set_can_be_untracked_run_count
        global fake_job_activity_exception_start_run_count
        global fake_server_repository_update_server_run_count
        global fake_job_repository_update_job_run_count
        global fake_job_repository_update_jobs_run_count
        global fake_job_repository_update_jobs_test_count
        global print_message_test

        fake_job_activity_start_run_count = 0
        fake_job_activity_set_job_run_count = 0
        fake_job_activity_set_can_be_untracked_run_count = 0
        fake_job_activity_exception_start_run_count = 0
        fake_server_repository_update_server_run_count = 0
        fake_job_repository_update_job_run_count = 0
        fake_job_repository_update_jobs_run_count = 0
        fake_job_repository_update_jobs_test_count = 0
        print_message_test = None

    def tearDownClass():
        global fake_job_activity_start_run_count
        global fake_job_activity_set_job_run_count
        global fake_job_activity_set_can_be_untracked_run_count
        global fake_job_activity_exception_start_run_count
        global fake_server_repository_update_server_run_count
        global fake_job_repository_update_job_run_count
        global fake_job_repository_update_jobs_run_count
        global fake_job_repository_update_jobs_test_count
        global print_message_test

        del(fake_job_activity_start_run_count)
        del(fake_job_activity_set_job_run_count)
        del(fake_job_activity_set_can_be_untracked_run_count)
        del(fake_job_activity_exception_start_run_count)
        del(fake_server_repository_update_server_run_count)
        del(fake_job_repository_update_job_run_count)
        del(fake_job_repository_update_jobs_run_count)
        del(fake_job_repository_update_jobs_test_count)
        del(print_message_test)

    @mock.patch(get_fully_qualified('run_enabled'), side_effect=[True, True, False])
    @mock.patch(get_fully_qualified('try_run_cycle'))
    @mock.patch(get_fully_qualified('sleep_cycle'))
    @mock.patch(get_fully_qualified('wait_until_slots_are_empty'))
    @mock.patch(get_fully_qualified('set_server_stop_state'))
    def test_run(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.run()
        self.assertEqual(get_call_count('run_enabled', args), 3)
        self.assertEqual(get_call_count('try_run_cycle', args), 2)
        self.assertEqual(get_call_count('sleep_cycle', args), 2)
        self.assertEqual(get_call_count('wait_until_slots_are_empty', args), 1)
        self.assertEqual(get_call_count('set_server_stop_state', args), 1)

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

    @mock.patch(get_fully_qualified('run_cycle'))
    def test_try_run_cycle(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.try_run_cycle()
        self.assertEqual(get_call_count('run_cycle', args), 1)

    @mock.patch(get_fully_qualified('run_cycle'), side_effect=Exception('run_cycle exception'))
    @mock.patch(get_fully_qualified('log'))
    def test_try_run_cycle_exception(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.try_run_cycle()
        actual_log = str(get_mock('log', args).call_args[0][0])
        self.assertTrue(actual_log.endswith('run_cycle exception'))
    
    @mock.patch(get_fully_qualified('set_server_cycle_state'))
    @mock.patch(get_fully_qualified('must_run_cycle_loop'), side_effect=[True, False])
    @mock.patch(get_fully_qualified('run_cycle_loop'))
    def test_run_cycle(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.run_cycle()
        self.assertEqual(get_call_count('set_server_cycle_state', args), 1)
        self.assertEqual(get_call_count('must_run_cycle_loop', args), 2)
        self.assertEqual(get_call_count('run_cycle_loop', args), 1)

    @mock.patch(get_fully_qualified('clear_finished_jobs'))
    @mock.patch(get_fully_qualified('wait_until_slot_is_open'))
    @mock.patch(get_fully_qualified('get_next_enqueued_job'), return_value=get_fake_job())
    @mock.patch(get_fully_qualified('try_set_lock_on_job'), return_value=True)
    @mock.patch(get_fully_qualified('run_job'))
    def test_run_cycle_loop(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.run_cycle_loop()
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
        self.assertEqual(get_call_count('wait_until_slot_is_open', args), 1)
        self.assertEqual(get_call_count('get_next_enqueued_job', args), 1)
        self.assertEqual(get_call_count('try_set_lock_on_job', args), 1)
        self.assertEqual(get_call_count('run_job', args), 1)

    @mock.patch(get_fully_qualified('clear_finished_jobs'))
    @mock.patch(get_fully_qualified('wait_until_slot_is_open'))
    @mock.patch(get_fully_qualified('get_next_enqueued_job'), return_value=None)
    @mock.patch(get_fully_qualified('try_set_lock_on_job'), return_value=True)
    @mock.patch(get_fully_qualified('run_job'))
    def test_run_cycle_loop_with_no_jobs_enqueued(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.run_cycle_loop()
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
        self.assertEqual(get_call_count('wait_until_slot_is_open', args), 1)
        self.assertEqual(get_call_count('get_next_enqueued_job', args), 1)
        self.assertEqual(get_call_count('try_set_lock_on_job', args), 0)
        self.assertEqual(get_call_count('run_job', args), 0)

    @mock.patch(get_fully_qualified('clear_finished_jobs'))
    @mock.patch(get_fully_qualified('wait_until_slot_is_open'))
    @mock.patch(get_fully_qualified('get_next_enqueued_job'), return_value=get_fake_job())
    @mock.patch(get_fully_qualified('try_set_lock_on_job'), return_value=False)
    @mock.patch(get_fully_qualified('run_job'))
    def test_run_cycle_loop_cannot_set_lock_on_job(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.run_cycle_loop()
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
        self.assertEqual(get_call_count('wait_until_slot_is_open', args), 1)
        self.assertEqual(get_call_count('get_next_enqueued_job', args), 1)
        self.assertEqual(get_call_count('try_set_lock_on_job', args), 1)
        self.assertEqual(get_call_count('run_job', args), 0)
    
    @mock.patch(get_fully_qualified('exists_enqueued_jobs'), side_effect=[False, False, False, False, True, True, True, True])
    @mock.patch(get_fully_qualified('slots_empty'), side_effect=[False, False, True, True, False, False, True, True])
    @mock.patch(get_fully_qualified('run_enabled'), side_effect=[False, True, False, True, False, True, False, True])
    def test_must_run_cycle_loop(self, *args):
        server_service = ServerService(None, None, None, None)
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertTrue(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertTrue(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertTrue(server_service.must_run_cycle_loop())

    @mock.patch(get_fully_qualified('slots_limit_reached'), side_effect=[True, False])
    @mock.patch(get_fully_qualified('clear_finished_jobs'))
    def test_wait_until_slot_is_open(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.wait_until_slot_is_open()
        self.assertEqual(get_call_count('slots_limit_reached', args), 2)
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
    
    @mock.patch(get_fully_qualified('slots_empty'), side_effect=[False, True])
    @mock.patch(get_fully_qualified('clear_finished_jobs'))
    def test_wait_until_slots_are_empty(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.wait_until_slots_are_empty()
        self.assertEqual(get_call_count('slots_empty', args), 2)
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)

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

    def test_slots_empty(self):
        server = Server(2)
        server_service = ServerService(server, None, None, None)
        job_activity = FakeJobActivity()
        server_service.job_activities_assigned.append(job_activity)
        self.assertFalse(server_service.slots_empty())
        server_service.job_activities_assigned.clear()
        self.assertTrue(server_service.slots_empty())

    @mock.patch(get_fully_qualified('save_finished_jobs'))
    @mock.patch(get_fully_qualified('untrack_jobs'))
    def test_clear_finished_jobs(self, *args):
        server_service = ServerService(None, None, None, None)
        server_service.clear_finished_jobs()
        self.assertEqual(get_call_count('save_finished_jobs', args), 1)
        self.assertEqual(get_call_count('untrack_jobs', args), 1)

    def test_save_finished_jobs(self):
        global fake_job_repository_update_jobs_run_count
        global fake_job_activity_set_can_be_untracked_run_count
        server_service = ServerService(None, None, None, FakeJobRepository())
        job_activity_running = FakeJobActivity()
        server_service.job_activities_assigned.append(job_activity_running)
        server_service.save_finished_jobs()
        self.assertEqual(fake_job_repository_update_jobs_run_count, 1)
        self.assertEqual(fake_job_repository_update_jobs_test_count, 0)

        job_activity_finished = FakeJobActivity()
        job_activity_finished._finished = True
        server_service.job_activities_assigned.append(job_activity_finished)
        server_service.save_finished_jobs()
        self.assertEqual(fake_job_repository_update_jobs_run_count, 2)
        self.assertEqual(fake_job_repository_update_jobs_test_count, 1)
        self.assertEqual(fake_job_activity_set_can_be_untracked_run_count, 1)
    
    def test_untrack_jobs(self):
        server_service = ServerService(None, None, None, None)
        job_activity_running = FakeJobActivity()
        server_service.job_activities_assigned.append(job_activity_running)
        server_service.untrack_jobs()
        self.assertEqual(len(server_service.job_activities_assigned), 1)

        job_activity_finished = FakeJobActivity()
        job_activity_finished._can_be_untracked = True
        server_service.job_activities_assigned.append(job_activity_finished)
        server_service.untrack_jobs()
        self.assertEqual(len(server_service.job_activities_assigned), 1)

    def test_exists_enqueued_jobs(self):
        mock_repository = types.SimpleNamespace()
        mock_repository.exists_jobs_with_status = mock.MagicMock(side_effect=[True, False])
        server_service = ServerService(None, None, None, mock_repository)
        self.assertTrue(server_service.exists_enqueued_jobs())
        self.assertFalse(server_service.exists_enqueued_jobs())

    def test_get_next_enqueued_job(self):
        server_service = ServerService(None, None, None, FakeJobRepository())
        enqueued_job = server_service.get_next_enqueued_job()
        self.assertIsNotNone(enqueued_job)
        self.assertIsInstance(enqueued_job, Job)

    @mock.patch(get_fully_qualified('set_job_start_state'))
    @mock.patch(get_fully_qualified('log'))
    @mock.patch(get_fully_qualified('get_job_activity_instance'), return_value=FakeJobActivity())
    @mock.patch(get_fully_qualified('add_job_activity_assigned'))
    def test_run_job(self, *args):
        global fake_job_activity_start_run_count
        server_service = ServerService(None, None, None, None)
        job = get_fake_job()
        server_service.run_job(job)
        self.assertEqual(get_call_count('set_job_start_state', args), 1)
        self.assertEqual(get_call_count('get_job_activity_instance', args), 1)
        self.assertEqual(get_call_count('add_job_activity_assigned', args), 1)
        self.assertEqual(fake_job_activity_start_run_count, 1)

    @mock.patch(get_fully_qualified('set_job_start_state'))
    @mock.patch(get_fully_qualified('log'))
    @mock.patch(get_fully_qualified('get_job_activity_instance'), return_value=FakeJobActivityException())
    @mock.patch(get_fully_qualified('add_job_activity_assigned'))
    def test_run_job_exception(self, *args):
        global fake_job_activity_exception_start_run_count
        server_service = ServerService(None, None, None, None)
        job = get_fake_job()
        server_service.run_job(job)
        self.assertEqual(get_call_count('set_job_start_state', args), 1)
        self.assertEqual(get_call_count('get_job_activity_instance', args), 1)
        self.assertEqual(get_call_count('add_job_activity_assigned', args), 1)
        self.assertEqual(fake_job_activity_exception_start_run_count, 1)
        actual_log = str(get_mock('log', args).call_args[0][0])
        self.assertTrue(actual_log.endswith('FakeJobActivityException exception'))
        pass

    def test_add_job_activity_assigned(self):
        server_service = ServerService(None, None, None, None)
        job_activity = FakeJobActivity()
        self.assertEqual(len(server_service.job_activities_assigned), 0)
        server_service.add_job_activity_assigned(job_activity)
        self.assertEqual(len(server_service.job_activities_assigned), 1)
        server_service.add_job_activity_assigned(job_activity)
        self.assertEqual(len(server_service.job_activities_assigned), 2)

    def test_get_job_activity_instance(self):
        global fake_job_activity_set_job_run_count
        server_service = ServerService(None, None, None, None)
        job = Job(FakeJobActivity().__module__, FakeJobActivity().__class__.__name__)
        job_instance = server_service.get_job_activity_instance(job)
        self.assertIsInstance(job_instance, FakeJobActivity)
        self.assertEqual(fake_job_activity_set_job_run_count, 1)

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
        job = get_fake_job()
        server_service = ServerService(None, None, None, FakeJobRepository())
        server_service.set_job_start_state(job)
        self.assertEqual(job.start_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(job.status, JobStatus.PROCESSING)
        self.assertEqual(fake_job_repository_update_job_run_count, 1)

    def test_try_set_lock_on_job(self):
        job_repository = FakeJobRepository()
        server_service = ServerService(None, None, None, job_repository)
        job = get_fake_job()
        job_repository.set_lock_return = True
        locked = server_service.try_set_lock_on_job(job)
        self.assertTrue(locked)
        job_repository.set_lock_return = False
        locked = server_service.try_set_lock_on_job(job)
        self.assertFalse(locked)

    @mock.patch('builtins.print', side_effect=print_side_effect)
    def test_log(self, print_mock):
        global print_message_test
        server_service = ServerService(None, None, None, None)
        server_service.log('some log message')
        self.assertEqual(print_message_test, 'some log message')

if (__name__ == "__main__"):
    main()