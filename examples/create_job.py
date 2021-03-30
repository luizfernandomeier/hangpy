import redis
from hangpy.repositories.redis_job_repository import RedisJobRepository
from jobs.job_print_date_time import JobPrintDateTime

job = JobPrintDateTime()

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = RedisJobRepository(redis_client)

job_repository.add_job(job)