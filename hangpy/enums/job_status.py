from enum import Enum

class JobStatus(Enum):
    ENQUEUED = 0
    PROCESSING = 10
    SUCCESS = 20
    ERROR = 99