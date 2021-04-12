import hangpy
import redis
import sys
from jobs.job_print_parameters import JobPrintParameters


redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = hangpy.RedisJobRepository(redis_client)

job_service = hangpy.JobService(job_repository)

job_service.enqueue_job(JobPrintParameters(), sys.argv[1:])
