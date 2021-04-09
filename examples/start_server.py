import hangpy
import redis

server_configuration = hangpy.ServerConfigurationDto(cycle_interval_milliseconds=10000, slots=10)

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = hangpy.RedisJobRepository(redis_client)
server_repository = hangpy.RedisServerRepository(redis_client)

server_service = hangpy.ServerService(server_configuration, server_repository, job_repository)

print('\nThe HangPy server is running!')
print(f'Server id: {server_service.server.id}')
print(f'Started: {server_service.server.start_datetime}')
print(f'Interval: {server_configuration.cycle_interval_milliseconds} ms')
print(f'Slots: {server_configuration.slots}')

server_service.start()

__exit = ''
while(__exit.lower() != 'exit'):
    __exit = input('\nTo exit the server, type \'exit\'.\n')

print('Shutdown in progress. Please wait..')

server_service.stop()

server_service.join()

print(f'Server {server_service.server.id} stopped.\n')
