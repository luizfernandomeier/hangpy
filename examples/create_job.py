from hangpy.repositories.redis_job_repository import RedisJobRepository
from jobs.job_print_date_time import JobPrintDateTime

job = JobPrintDateTime()

job_repository = RedisJobRepository('172.17.0.1', 6379)

job_repository.add_job(job)