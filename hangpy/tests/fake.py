from hangpy.services import JobActivityBase

fake_job_action_result = ''

class FakeJob(JobActivityBase):
    def action(self):
        global fake_job_action_result
        fake_job_action_result = "executed the action"

class FakeJobException(JobActivityBase):
    def action(self):
        raise Exception('fake job exception message')

class FakeAbstractJob(JobActivityBase):
    def action(self):
        return JobActivityBase.action(self)