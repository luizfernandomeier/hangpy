from hangpy.services import JobActivityBase

fake_job_action_result = ''

class FakeJob(JobActivityBase):
    def action(self):
        global fake_job_action_result
        fake_job_action_result = "executed the action"

class FakeAbstractJob(JobActivityBase):
    def action(self):
        return JobActivityBase.action(self)