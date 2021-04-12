from freezegun import freeze_time
from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.services import JobActivityBase
from hangpy.tests.fake import FakeJobActivity
from unittest import TestCase, mock, main


def get_fully_qualified_name(method_mocked: str) -> str:
    return f'hangpy.services.job_activity_base.JobActivityBase.{method_mocked}'


def get_mock(method_mocked: str, args) -> mock.MagicMock:
    return next(mock for mock in args if f'name=\'{method_mocked}\'' in str(mock))


def get_call_count(method_mocked: str, args) -> int:
    return get_mock(method_mocked, args).call_count


class TestJobActivityBase(TestCase):

    def test_action(self):
        class FakeAbstractJob(JobActivityBase):
            def action(self):
                return JobActivityBase.action(self)
        self.assertIsNone(FakeAbstractJob().action())

    @mock.patch(get_fully_qualified_name('set_job_status'))
    @mock.patch(get_fully_qualified_name('set_job_error'))
    @mock.patch(get_fully_qualified_name('set_job_end_datetime'))
    @mock.patch(get_fully_qualified_name('set_started_to_run'))
    def test_start(self, *args):
        job_activity = FakeJobActivity()
        job_activity.action = mock.MagicMock()
        self.assertEqual(job_activity.action.call_count, 0)
        job_activity.start()
        job_activity.join()
        self.assertEqual(job_activity.action.call_count, 1)
        self.assertEqual(get_call_count('set_job_status', args), 1)
        self.assertEqual(get_call_count('set_job_error', args), 0)
        self.assertEqual(get_call_count('set_job_end_datetime', args), 1)
        self.assertEqual(get_call_count('set_started_to_run', args), 1)

    @mock.patch(get_fully_qualified_name('set_job_status'))
    @mock.patch(get_fully_qualified_name('set_job_error'))
    @mock.patch(get_fully_qualified_name('set_job_end_datetime'))
    @mock.patch(get_fully_qualified_name('set_started_to_run'))
    def test_start_exception(self, *args):
        job_activity = FakeJobActivity()
        job_activity.action = mock.MagicMock(side_effect=Exception())
        job_activity.start()
        job_activity.join()
        self.assertEqual(get_call_count('set_job_status', args), 1)
        self.assertEqual(get_call_count('set_job_error', args), 1)
        self.assertEqual(get_call_count('set_job_end_datetime', args), 1)
        self.assertEqual(get_call_count('set_started_to_run', args), 1)

    def test_create_job_object(self):
        job_activity = FakeJobActivity()
        actual_job = job_activity.create_job_object()
        self.assertTrue(actual_job.module_name.endswith('fake'))
        self.assertEqual(actual_job.class_name, 'FakeJobActivity')

        actual_job = job_activity.create_job_object(['a', 'b'])
        self.assertListEqual(actual_job.parameters, ['a', 'b'])

    def test_set_job(self):
        job_activity = FakeJobActivity()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertEqual(job_activity._job, job)

    def test_get_job(self):
        job_activity = FakeJobActivity()
        job = Job('some_module', 'some_class')
        job_activity._job = job
        actual_job = job_activity.get_job()
        self.assertEqual(actual_job, job)

    def test_set_started_to_run(self):
        job_activity = FakeJobActivity()
        self.assertFalse(job_activity._started_to_run)
        job_activity.set_started_to_run()
        self.assertTrue(job_activity._started_to_run)

    def test_is_finished(self):
        job_activity = FakeJobActivity()
        self.assertFalse(job_activity.is_finished())
        job_activity._started_to_run = True
        self.assertTrue(job_activity.is_finished())

    def test_set_can_be_untracked(self):
        job_activity = FakeJobActivity()
        self.assertFalse(job_activity._can_be_untracked)
        job_activity.set_can_be_untracked()
        self.assertTrue(job_activity._can_be_untracked)

    def test_can_be_untracked(self):
        job_activity = FakeJobActivity()
        self.assertFalse(job_activity.can_be_untracked())
        job_activity._can_be_untracked = True
        self.assertTrue(job_activity.can_be_untracked())

    @mock.patch(get_fully_qualified_name('is_alive'), return_value=True)
    def test_is_finished_thread_running(self, is_alive_mock):
        job_activity = FakeJobActivity()
        self.assertFalse(job_activity.is_finished())
        job_activity._started_to_run = True
        self.assertFalse(job_activity.is_finished())

    def test_set_job_status(self):
        job_activity = FakeJobActivity()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertEqual(job_activity._job.status, JobStatus.ENQUEUED)
        job_activity.set_job_status(JobStatus.PROCESSING)
        self.assertEqual(job_activity._job.status, JobStatus.PROCESSING)

    def test_set_job_error(self):
        job_activity = FakeJobActivity()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertIsNone(job_activity._job.error)
        job_activity.set_job_error(Exception('some exception message'))
        self.assertEqual(job_activity._job.error, 'some exception message')

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_job_end_datetime(self):
        job_activity = FakeJobActivity()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertIsNone(job_activity._job.end_datetime)
        job_activity.set_job_end_datetime()
        self.assertEqual(job_activity._job.end_datetime, '1988-04-10T11:01:02.123456')


if (__name__ == "__main__"):
    main()
