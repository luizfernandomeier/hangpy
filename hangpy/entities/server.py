import datetime
import uuid


class Server():

    def __init__(self, slots=10):
        self.id = str(uuid.uuid4())
        self.start_datetime = datetime.datetime.now().isoformat()
        self.stop_datetime = None
        self.last_cycle_datetime = None
        self.slots = slots
