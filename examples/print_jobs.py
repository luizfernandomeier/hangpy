import redis
from hangpy.repositories.redis_job_repository import RedisJobRepository

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = RedisJobRepository(redis_client)

for job in job_repository.get_jobs():
    print(f'\nid: {job.id}')
    print(f'module_name: {job.module_name}')
    print(f'class_name: {job.class_name}')
    print(f'status: {job.status}')
    print(f'enqueued_datetime: {job.enqueued_datetime}')
    print(f'start_datetime: {job.start_datetime}')
    print(f'end_datetime: {job.end_datetime}')
