import datetime
from hangpy import JobActivityBase


class JobPrintDateTime(JobActivityBase):

    def action(self):
        print(datetime.datetime.now())
