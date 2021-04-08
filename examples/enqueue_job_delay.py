import redis
import sys
from hangpy.repositories.redis_job_repository import RedisJobRepository
from jobs.job_delay import JobDelay

jobs_quantity = int(sys.argv[1])

job = JobDelay()

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = RedisJobRepository(redis_client)

for job_index in range(jobs_quantity):
    job_repository.add_job(job)
