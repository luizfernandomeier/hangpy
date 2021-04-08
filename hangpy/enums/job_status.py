from enum import Enum


class JobStatus(Enum):
    """Enumeration containing the possible status for a job."""

    ENQUEUED = 0
    PROCESSING = 10
    SUCCESS = 20
    ERROR = 99
