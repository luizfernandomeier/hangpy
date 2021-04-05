import hangpy
import redis
import sys

slots = int(sys.argv[1])

server_configuration = hangpy.ServerConfigurationDto()
server = hangpy.Server(slots)

print('\nThe HangPy server is running!')
print(f'Server id: {server.id}')
print(f'Started: {server.start_datetime}')
print(f'Interval: {server_configuration.cycle_interval_milliseconds} ms')

redis_client = redis.StrictRedis(host='172.17.0.1', port=6379, password=None)

job_repository = hangpy.RedisJobRepository(redis_client)
server_repository = hangpy.RedisServerRepository(redis_client)

server_repository.add_server(server)

server_service = hangpy.ServerService(server, server_configuration, server_repository, job_repository)

exit_message = "To exit the server, type 'exit'."
print(f'\n{exit_message}')

server_service.start()

__exit = input()

while(__exit.lower() != 'exit'):
    __exit = input(f'\n{exit_message}')

print('Shutdown in progress. Please wait..')

server_service.stop_signal = True

server_service.join()

print(f'Server {server.id} stopped.\n')