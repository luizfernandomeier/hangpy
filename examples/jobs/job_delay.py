import datetime
import time
from hangpy import JobActivityBase


class JobDelay(JobActivityBase):

    def action(self):
        print(f'starting job \'{self.get_job().id}\' - {datetime.datetime.now()}')
        time.sleep(10)
        print(f'finished job \'{self.get_job().id}\' - {datetime.datetime.now()}')
