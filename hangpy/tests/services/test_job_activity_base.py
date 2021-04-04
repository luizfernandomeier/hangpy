import hangpy.tests.fake as fake
from freezegun import freeze_time
from hangpy.entities import Job
from hangpy.enums import JobStatus
from hangpy.services import JobActivityBase
from unittest import TestCase, mock, main

def set_job_status_side_effect(*args):
    global set_job_status_run_count
    set_job_status_run_count += 1

def set_job_error_side_effect(*args):
    global set_job_error_run_count
    set_job_error_run_count += 1

def set_job_end_datetime_side_effect(*args):
    global set_job_end_datetime_run_count
    set_job_end_datetime_run_count += 1

class TestJobActivityBase(TestCase):

    def setUp(self):
        global set_job_status_run_count
        global set_job_error_run_count
        global set_job_end_datetime_run_count
        set_job_status_run_count = 0
        set_job_error_run_count = 0
        set_job_end_datetime_run_count = 0

    def tearDownClass():
        global set_job_status_run_count
        global set_job_error_run_count
        global set_job_end_datetime_run_count
        del(set_job_status_run_count)
        del(set_job_error_run_count)
        del(set_job_end_datetime_run_count)

    def test_action(self):
        fake_abstract_job = fake.FakeAbstractJob()
        self.assertIsNone(fake_abstract_job.action())

    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.set_job_status', side_effect=set_job_status_side_effect)
    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.set_job_error', side_effect=set_job_error_side_effect)
    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.set_job_end_datetime', side_effect=set_job_end_datetime_side_effect)
    def test_start(self, set_job_status_mock, set_job_error_mock, set_job_end_datetime_mock):
        global set_job_status_run_count
        global set_job_error_run_count
        global set_job_end_datetime_run_count
        fake.fake_job_action_result = None
        job_activity = fake.FakeJob()
        job_activity.start()
        expected = "executed the action"
        job_activity.join()
        self.assertEqual(fake.fake_job_action_result, expected)
        self.assertEqual(set_job_status_run_count, 1)
        self.assertEqual(set_job_error_run_count, 0)
        self.assertEqual(set_job_end_datetime_run_count, 1)

    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.set_job_status', side_effect=set_job_status_side_effect)
    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.set_job_error', side_effect=set_job_error_side_effect)
    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.set_job_end_datetime', side_effect=set_job_end_datetime_side_effect)
    def test_start_exception(self, set_job_status_mock, set_job_error_mock, set_job_end_datetime_mock):
        global set_job_status_run_count
        global set_job_error_run_count
        global set_job_end_datetime_run_count
        job_activity = fake.FakeJobException()
        job_activity.start()
        job_activity.join()
        self.assertEqual(set_job_status_run_count, 1)
        self.assertEqual(set_job_error_run_count, 1)
        self.assertEqual(set_job_end_datetime_run_count, 1)

    def test_get_job_object(self):
        job_activity = fake.FakeJob()
        job = job_activity.get_job_object()
        self.assertTrue(job.module_name.endswith('fake'))
        self.assertEqual(job.class_name, 'FakeJob')

    def test_set_job(self):
        job_activity = fake.FakeJob()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertEqual(job_activity._job, job)

    def test_get_job(self):
        job_activity = fake.FakeJob()
        job = Job('some_module', 'some_class')
        job_activity._job = job
        actual_job = job_activity.get_job()
        self.assertEqual(actual_job, job)
    
    def test_set_started_to_run(self):
        job_activity = fake.FakeJob()
        self.assertFalse(job_activity._started_to_run)
        
        job_activity.set_started_to_run()
        self.assertTrue(job_activity._started_to_run)

    def test_is_finished(self):
        job_activity = fake.FakeJob()
        self.assertFalse(job_activity.is_finished())

        job_activity._started_to_run = True
        self.assertTrue(job_activity.is_finished())

    @mock.patch('hangpy.services.job_activity_base.JobActivityBase.is_alive', return_value=True)
    def test_is_finished_thread_running(self, is_alive_mock):
        job_activity = fake.FakeJob()
        self.assertFalse(job_activity.is_finished())

        job_activity._started_to_run = True
        self.assertFalse(job_activity.is_finished())

    def test_set_job_status(self):
        job_activity = fake.FakeJob()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertEqual(job_activity._job.status, JobStatus.ENQUEUED)

        job_activity.set_job_status(JobStatus.PROCESSING)
        self.assertEqual(job_activity._job.status, JobStatus.PROCESSING)
    
    def test_set_job_error(self):
        job_activity = fake.FakeJob()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertIsNone(job_activity._job.error)

        job_activity.set_job_error(Exception('some exception message'))
        self.assertEqual(job_activity._job.error, 'some exception message')

    @freeze_time('1988-04-10 11:01:02.123456')
    def test_set_job_end_datetime(self):
        job_activity = fake.FakeJob()
        job = Job('some_module', 'some_class')
        job_activity.set_job(job)
        self.assertIsNone(job_activity._job.end_datetime)

        job_activity.set_job_end_datetime()
        self.assertEqual(job_activity._job.end_datetime, '1988-04-10T11:01:02.123456')

if (__name__ == "__main__"):
    main()