import datetime
import types
from freezegun import freeze_time
from hangpy.dtos import ServerConfigurationDto
from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.services import JobActivityBase, ServerService
from unittest import TestCase, mock, main


def get_fully_qualified_name(method_mocked: str) -> str:
    return f'hangpy.services.server_service.ServerService.{method_mocked}'


def get_mock(method_mocked: str, args) -> mock.MagicMock:
    return next(mock for mock in args if f'name=\'{method_mocked}\'' in str(mock))


def get_call_count(method_mocked: str, args) -> int:
    return get_mock(method_mocked, args).call_count


def get_fake_job() -> Job:
    return Job('module_test', 'class_test')


class FakeJobActivity(JobActivityBase):

    def __init__(self):
        self.set_job = mock.MagicMock()
        JobActivityBase.__init__(self)

    def action(self):
        pass


class TestServerService(TestCase):

    @mock.patch(get_fully_qualified_name('set_server_start_state'))
    @mock.patch(get_fully_qualified_name('log_run'))
    @mock.patch(get_fully_qualified_name('run_enabled'), side_effect=[True, True, False])
    @mock.patch(get_fully_qualified_name('try_run_cycle'))
    @mock.patch(get_fully_qualified_name('sleep_cycle'))
    @mock.patch(get_fully_qualified_name('wait_until_slots_are_empty'))
    @mock.patch(get_fully_qualified_name('set_server_stop_state'))
    def test_run(self, *args):
        server_service = ServerService(None, None, None)
        server_service.run()
        self.assertEqual(get_call_count('set_server_start_state', args), 1)
        self.assertEqual(get_call_count('run_enabled', args), 3)
        self.assertEqual(get_call_count('try_run_cycle', args), 2)
        self.assertEqual(get_call_count('sleep_cycle', args), 2)
        self.assertEqual(get_call_count('wait_until_slots_are_empty', args), 1)
        self.assertEqual(get_call_count('set_server_stop_state', args), 1)

    @mock.patch(get_fully_qualified_name('log'))
    def test_log_run(self, *args):
        server_service = ServerService(ServerConfigurationDto(), None, None)
        server_service.log_run()
        self.assertEqual(get_call_count('log', args), 1)

    def test_sleep_cycle(self):
        server_service = ServerService(ServerConfigurationDto(1000), None, None)
        time_start = datetime.datetime.now()
        server_service.sleep_cycle()
        time_stop = datetime.datetime.now()
        total_milliseconds = (time_stop - time_start).seconds * 1000
        total_milliseconds += (time_stop - time_start).microseconds / 1000
        self.assertGreater(total_milliseconds, 1000)

    def test_run_enabled(self):
        server_service = ServerService(None, None, None)
        server_service.stop_signal = False
        self.assertTrue(server_service.run_enabled())
        server_service.stop_signal = True
        self.assertFalse(server_service.run_enabled())

    @mock.patch(get_fully_qualified_name('run_cycle'))
    def test_try_run_cycle(self, *args):
        server_service = ServerService(None, None, None)
        server_service.try_run_cycle()
        self.assertEqual(get_call_count('run_cycle', args), 1)

    @mock.patch(get_fully_qualified_name('run_cycle'), side_effect=Exception('run_cycle exception'))
    @mock.patch(get_fully_qualified_name('log'))
    def test_try_run_cycle_exception(self, *args):
        server_service = ServerService(None, None, None)
        server_service.try_run_cycle()
        actual_log = str(get_mock('log', args).call_args[0][0])
        self.assertTrue(actual_log.endswith('run_cycle exception'))

    @mock.patch(get_fully_qualified_name('set_server_cycle_state'))
    @mock.patch(get_fully_qualified_name('must_run_cycle_loop'), side_effect=[True, False])
    @mock.patch(get_fully_qualified_name('run_cycle_loop'))
    def test_run_cycle(self, *args):
        server_service = ServerService(None, None, None)
        server_service.run_cycle()
        self.assertEqual(get_call_count('set_server_cycle_state', args), 1)
        self.assertEqual(get_call_count('must_run_cycle_loop', args), 2)
        self.assertEqual(get_call_count('run_cycle_loop', args), 1)

    @mock.patch(get_fully_qualified_name('clear_finished_jobs'))
    @mock.patch(get_fully_qualified_name('wait_until_slot_is_open'))
    @mock.patch(get_fully_qualified_name('get_next_enqueued_job'), return_value=get_fake_job())
    @mock.patch(get_fully_qualified_name('try_set_lock_on_job'), return_value=True)
    @mock.patch(get_fully_qualified_name('run_job'))
    def test_run_cycle_loop(self, *args):
        server_service = ServerService(None, None, None)
        server_service.run_cycle_loop()
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
        self.assertEqual(get_call_count('wait_until_slot_is_open', args), 1)
        self.assertEqual(get_call_count('get_next_enqueued_job', args), 1)
        self.assertEqual(get_call_count('try_set_lock_on_job', args), 1)
        self.assertEqual(get_call_count('run_job', args), 1)

    @mock.patch(get_fully_qualified_name('clear_finished_jobs'))
    @mock.patch(get_fully_qualified_name('wait_until_slot_is_open'))
    @mock.patch(get_fully_qualified_name('get_next_enqueued_job'), return_value=None)
    @mock.patch(get_fully_qualified_name('try_set_lock_on_job'), return_value=True)
    @mock.patch(get_fully_qualified_name('run_job'))
    def test_run_cycle_loop_with_no_jobs_enqueued(self, *args):
        server_service = ServerService(None, None, None)
        server_service.run_cycle_loop()
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
        self.assertEqual(get_call_count('wait_until_slot_is_open', args), 1)
        self.assertEqual(get_call_count('get_next_enqueued_job', args), 1)
        self.assertEqual(get_call_count('try_set_lock_on_job', args), 0)
        self.assertEqual(get_call_count('run_job', args), 0)

    @mock.patch(get_fully_qualified_name('clear_finished_jobs'))
    @mock.patch(get_fully_qualified_name('wait_until_slot_is_open'))
    @mock.patch(get_fully_qualified_name('get_next_enqueued_job'), return_value=get_fake_job())
    @mock.patch(get_fully_qualified_name('try_set_lock_on_job'), return_value=False)
    @mock.patch(get_fully_qualified_name('run_job'))
    def test_run_cycle_loop_cannot_set_lock_on_job(self, *args):
        server_service = ServerService(None, None, None)
        server_service.run_cycle_loop()
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)
        self.assertEqual(get_call_count('wait_until_slot_is_open', args), 1)
        self.assertEqual(get_call_count('get_next_enqueued_job', args), 1)
        self.assertEqual(get_call_count('try_set_lock_on_job', args), 1)
        self.assertEqual(get_call_count('run_job', args), 0)

    @mock.patch(get_fully_qualified_name('exists_enqueued_jobs'), side_effect=[False, False, False, False, True, True, True, True])
    @mock.patch(get_fully_qualified_name('slots_empty'), side_effect=[False, False, True, True, False, False, True, True])
    @mock.patch(get_fully_qualified_name('run_enabled'), side_effect=[False, True, False, True, False, True, False, True])
    def test_must_run_cycle_loop(self, *args):
        server_service = ServerService(None, None, None)
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertTrue(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertTrue(server_service.must_run_cycle_loop())
        self.assertFalse(server_service.must_run_cycle_loop())
        self.assertTrue(server_service.must_run_cycle_loop())

    @mock.patch(get_fully_qualified_name('slots_limit_reached'), side_effect=[True, False])
    @mock.patch(get_fully_qualified_name('clear_finished_jobs'))
    def test_wait_until_slot_is_open(self, *args):
        server_service = ServerService(None, None, None)
        server_service.wait_until_slot_is_open()
        self.assertEqual(get_call_count('slots_limit_reached', args), 2)
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)

    @mock.patch(get_fully_qualified_name('slots_empty'), side_effect=[False, True])
    @mock.patch(get_fully_qualified_name('clear_finished_jobs'))
    def test_wait_until_slots_are_empty(self, *args):
        server_service = ServerService(None, None, None)
        server_service.wait_until_slots_are_empty()
        self.assertEqual(get_call_count('slots_empty', args), 2)
        self.assertEqual(get_call_count('clear_finished_jobs', args), 1)

    def test_slots_limit_reached(self):
        server_configuration = ServerConfigurationDto(slots=2)
        server_service = ServerService(server_configuration, None, None)
        job_activity = mock.MagicMock(spec=JobActivityBase)
        server_service.job_activities_assigned.append(job_activity)
        self.assertFalse(server_service.slots_limit_reached())
        server_service.job_activities_assigned.append(job_activity)
        self.assertTrue(server_service.slots_limit_reached())
        server_service.job_activities_assigned.append(job_activity)
        self.assertTrue(server_service.slots_limit_reached())
        server_service.job_activities_assigned.clear()
        self.assertFalse(server_service.slots_limit_reached())

    def test_slots_empty(self):
        server_configuration = ServerConfigurationDto(slots=2)
        server_service = ServerService(server_configuration, None, None)
        job_activity = mock.MagicMock(spec=JobActivityBase)
        server_service.job_activities_assigned.append(job_activity)
        self.assertFalse(server_service.slots_empty())
        server_service.job_activities_assigned.clear()
        self.assertTrue(server_service.slots_empty())

    @mock.patch(get_fully_qualified_name('save_finished_jobs'))
    @mock.patch(get_fully_qualified_name('untrack_jobs'))
    def test_clear_finished_jobs(self, *args):
        server_service = ServerService(None, None, None)
        server_service.clear_finished_jobs()
        self.assertEqual(get_call_count('save_finished_jobs', args), 1)
        self.assertEqual(get_call_count('untrack_jobs', args), 1)

    def test_save_finished_jobs(self):
        jobs_updated = 0

        def fake_update_jobs(jobs):
            nonlocal jobs_updated
            jobs_updated += len(jobs)

        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.update_jobs = mock.MagicMock(side_effect=fake_update_jobs)
        server_service = ServerService(None, None, fake_job_repository)
        job_activity_running = types.SimpleNamespace()
        job_activity_running.is_finished = mock.MagicMock(return_value=False)
        job_activity_running.get_job = mock.MagicMock(return_value=get_fake_job())
        job_activity_running.set_can_be_untracked = mock.MagicMock()
        server_service.job_activities_assigned.append(job_activity_running)
        server_service.save_finished_jobs()
        self.assertEqual(fake_job_repository.update_jobs.call_count, 1)
        self.assertEqual(jobs_updated, 0)
        self.assertEqual(job_activity_running.set_can_be_untracked.call_count, 0)

        job_activity_finished = types.SimpleNamespace()
        job_activity_finished.is_finished = mock.MagicMock(return_value=True)
        job_activity_finished.get_job = mock.MagicMock(return_value=get_fake_job())
        job_activity_finished.set_can_be_untracked = mock.MagicMock()
        server_service.job_activities_assigned.append(job_activity_finished)
        server_service.save_finished_jobs()
        self.assertEqual(fake_job_repository.update_jobs.call_count, 2)
        self.assertEqual(jobs_updated, 1)
        self.assertEqual(job_activity_finished.set_can_be_untracked.call_count, 1)

    def test_untrack_jobs(self):
        server_service = ServerService(None, None, None)
        job_activity_running = types.SimpleNamespace()
        job_activity_running.can_be_untracked = mock.MagicMock(return_value=False)
        server_service.job_activities_assigned.append(job_activity_running)
        self.assertEqual(len(server_service.job_activities_assigned), 1)
        server_service.untrack_jobs()
        self.assertEqual(len(server_service.job_activities_assigned), 1)

        job_activity_finished = types.SimpleNamespace()
        job_activity_finished.can_be_untracked = mock.MagicMock(return_value=True)
        server_service.job_activities_assigned.append(job_activity_finished)
        self.assertEqual(len(server_service.job_activities_assigned), 2)
        server_service.untrack_jobs()
        self.assertEqual(len(server_service.job_activities_assigned), 1)

    def test_exists_enqueued_jobs(self):
        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.exists_jobs_with_status = mock.MagicMock(side_effect=[True, False])
        server_service = ServerService(None, None, fake_job_repository)
        self.assertTrue(server_service.exists_enqueued_jobs())
        self.assertFalse(server_service.exists_enqueued_jobs())

    def test_get_next_enqueued_job(self):
        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.get_job_by_status = mock.MagicMock(return_value=get_fake_job())
        server_service = ServerService(None, None, fake_job_repository)
        enqueued_job = server_service.get_next_enqueued_job()
        self.assertIsNotNone(enqueued_job)
        self.assertIsInstance(enqueued_job, Job)

    @mock.patch(get_fully_qualified_name('set_job_start_state'))
    @mock.patch(get_fully_qualified_name('log'))
    @mock.patch(get_fully_qualified_name('get_job_activity_instance'))
    @mock.patch(get_fully_qualified_name('add_job_activity_assigned'))
    @mock.patch(get_fully_qualified_name('run_job_instance'))
    def test_run_job(self, *args):
        server_service = ServerService(None, None, None)
        job = get_fake_job()
        server_service.run_job(job)
        self.assertEqual(get_call_count('set_job_start_state', args), 1)
        self.assertEqual(get_call_count('get_job_activity_instance', args), 1)
        self.assertEqual(get_call_count('add_job_activity_assigned', args), 1)
        self.assertEqual(get_call_count('run_job_instance', args), 1)

    @mock.patch(get_fully_qualified_name('set_job_start_state'))
    @mock.patch(get_fully_qualified_name('log'))
    @mock.patch(get_fully_qualified_name('get_job_activity_instance'))
    @mock.patch(get_fully_qualified_name('add_job_activity_assigned'))
    @mock.patch(get_fully_qualified_name('run_job_instance'), side_effect=Exception('run_job_instance exception'))
    def test_run_job_exception(self, *args):
        server_service = ServerService(None, None, None)
        job = get_fake_job()
        server_service.run_job(job)
        self.assertEqual(get_call_count('set_job_start_state', args), 1)
        self.assertEqual(get_call_count('get_job_activity_instance', args), 1)
        self.assertEqual(get_call_count('add_job_activity_assigned', args), 1)
        self.assertEqual(get_call_count('run_job_instance', args), 1)
        actual_log = str(get_mock('log', args).call_args[0][0])
        self.assertTrue(actual_log.endswith('run_job_instance exception'))

    def test_run_job_instance(self):
        server_service = ServerService(None, None, None)
        job_activity = mock.MagicMock(spec=JobActivityBase)
        job_activity.start = mock.MagicMock()
        self.assertEqual(job_activity.start.call_count, 0)
        server_service.run_job_instance(job_activity)
        self.assertEqual(job_activity.start.call_count, 1)

    def test_add_job_activity_assigned(self):
        server_service = ServerService(None, None, None)
        job_activity = types.SimpleNamespace()
        self.assertEqual(len(server_service.job_activities_assigned), 0)
        server_service.add_job_activity_assigned(job_activity)
        self.assertEqual(len(server_service.job_activities_assigned), 1)
        server_service.add_job_activity_assigned(job_activity)
        self.assertEqual(len(server_service.job_activities_assigned), 2)

    def test_get_job_activity_instance(self):
        server_service = ServerService(None, None, None)
        fake_job_activity = FakeJobActivity()
        job = Job(fake_job_activity.__module__, fake_job_activity.__class__.__name__)
        job_instance = server_service.get_job_activity_instance(job)
        self.assertIsInstance(job_instance, FakeJobActivity)
        self.assertEqual(job_instance.set_job.call_count, 1)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_server_start_state(self):
        fake_server_repository = types.SimpleNamespace()
        fake_server_repository.add_server = mock.MagicMock()
        server_service = ServerService(ServerConfigurationDto(), fake_server_repository, None)
        self.assertIsNone(server_service.server.start_datetime)
        server_service.set_server_start_state()
        self.assertEqual(server_service.server.start_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(fake_server_repository.add_server.call_count, 1)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_server_cycle_state(self):
        fake_server_repository = types.SimpleNamespace()
        fake_server_repository.update_server = mock.MagicMock()
        server_service = ServerService(ServerConfigurationDto(), fake_server_repository, None)
        self.assertIsNone(server_service.server.last_cycle_datetime)
        server_service.set_server_cycle_state()
        self.assertEqual(server_service.server.last_cycle_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(fake_server_repository.update_server.call_count, 1)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_server_stop_state(self):
        fake_server_repository = types.SimpleNamespace()
        fake_server_repository.update_server = mock.MagicMock()
        server_service = ServerService(ServerConfigurationDto(), fake_server_repository, None)
        self.assertIsNone(server_service.server.stop_datetime)
        server_service.set_server_stop_state()
        self.assertEqual(server_service.server.stop_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(fake_server_repository.update_server.call_count, 1)

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_job_start_state(self):
        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.update_job = mock.MagicMock()
        job = get_fake_job()
        server_service = ServerService(None, None, fake_job_repository)
        server_service.set_job_start_state(job)
        self.assertEqual(job.start_datetime, '1988-04-10T11:01:02.123456')
        self.assertEqual(job.status, JobStatus.PROCESSING)
        self.assertEqual(fake_job_repository.update_job.call_count, 1)

    def test_try_set_lock_on_job(self):
        fake_job_repository = types.SimpleNamespace()
        fake_job_repository.try_set_lock_on_job = mock.MagicMock(side_effect=[True, False])
        server_service = ServerService(None, None, fake_job_repository)
        job = get_fake_job()
        self.assertTrue(server_service.try_set_lock_on_job(job))
        self.assertFalse(server_service.try_set_lock_on_job(job))

    @mock.patch(get_fully_qualified_name('log_stop'))
    def test_stop(self, *args):
        server_service = ServerService(None, None, None)
        self.assertFalse(server_service.stop_signal)
        server_service.stop()
        self.assertTrue(server_service.stop_signal)

    @mock.patch(get_fully_qualified_name('log'))
    def test_log_stop(self, *args):
        server_service = ServerService(None, None, None)
        server_service.log_stop()
        self.assertEqual(get_call_count('log', args), 1)

    @mock.patch(get_fully_qualified_name('log_join'))
    @mock.patch('threading.Thread.join')
    def test_join(self, *args):
        server_service = ServerService(None, None, None)
        server_service.join()
        self.assertEqual(get_call_count('join', args), 1)

    @mock.patch(get_fully_qualified_name('log'))
    def test_log_join(self, *args):
        server_service = ServerService(None, None, None)
        server_service.log_join()
        self.assertEqual(get_call_count('log', args), 1)

    def test_log_with_logger_injected(self):
        fake_log_service = types.SimpleNamespace()
        fake_log_service.log = mock.MagicMock()
        server_service = ServerService(None, None, None, fake_log_service)
        server_service.log('some log message')
        self.assertEqual(fake_log_service.log.call_args[0][0], 'some log message')

    def test_log_without_logger_injected(self):
        fake_log_service = types.SimpleNamespace()
        fake_log_service.log = mock.MagicMock()
        server_service = ServerService(None, None, None)
        server_service.log('some log message')
        self.assertEqual(fake_log_service.log.call_count, 0)


if (__name__ == "__main__"):
    main()
