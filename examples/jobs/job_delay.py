from hangpy.services.job_activity_base import JobActivityBase
import datetime
import time


class JobDelay(JobActivityBase):

    def action(self):
        print(f'starting job \'{self.get_job().id}\' - {datetime.datetime.now()}')
        time.sleep(10)
        print(f'finished job \'{self.get_job().id}\' - {datetime.datetime.now()}')
