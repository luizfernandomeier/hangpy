from hangpy import JobActivityBase


class JobPrintParameters(JobActivityBase):

    def action(self):
        print(f'This is what you have sent me: {self.get_job().parameters}')
