from hangpy.services.job_activity_base import JobActivityBase
import datetime

class JobPrintDateTime(JobActivityBase):

    def action(self):
        print(datetime.datetime.now())
