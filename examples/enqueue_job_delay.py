import hangpy
import redis
import sys
from jobs.job_delay import JobDelay

jobs_quantity = int(sys.argv[1])

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = hangpy.RedisJobRepository(redis_client)

job_service = hangpy.JobService(job_repository)

for job_index in range(jobs_quantity):
    job_service.enqueue_job(JobDelay())
