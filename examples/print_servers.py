from hangpy.repositories.redis_server_repository import RedisServerRepository

server_repository = RedisServerRepository('172.17.0.1', 6379)

for server in server_repository.get_servers():
    print(f'\nid: {server.id}')
    print(f'start_datetime: {server.start_datetime}')
    print(f'stop_datetime: {server.stop_datetime}')
    print(f'last_cycle_datetime: {server.last_cycle_datetime}')