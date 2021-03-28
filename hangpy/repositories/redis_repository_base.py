import jsonpickle
import redis

class RedisRepositoryBase():

    def __init__(self, host, port, password=None):
        self.client = redis.Redis(host=host, port=port, password=password)

    def _get_keys(self, match):
        keys = []
        cursor, result_keys = self.client.scan(cursor=0, match=match)
        keys.extend(result_keys)
        while (cursor != 0):
            cursor, result_keys = self.client.scan(cursor=cursor, match=match)
            keys.extend(result_keys)
        return keys

    def _deserialize_entries(self, serialized_entries):
        return [jsonpickle.decode(serialized_entry) for serialized_entry in serialized_entries]