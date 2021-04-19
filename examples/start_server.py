import hangpy
import redis

server_configuration = hangpy.ServerConfigurationDto(cycle_interval_milliseconds=10000, slots=10)

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = hangpy.RedisJobRepository(redis_client)
server_repository = hangpy.RedisServerRepository(redis_client)
log_service = hangpy.PrintLogService()

server_service = hangpy.ServerService(server_configuration, server_repository, job_repository, log_service)

server_service.start()

__exit = ''
while(__exit.lower() != 'exit'):
    __exit = input('\nTo exit the server, type \'exit\'.\n')

server_service.stop()

server_service.join()
