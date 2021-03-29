import jsonpickle

class RedisRepositoryBase():

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def _get_keys(self, match):
        keys = []
        cursor, result_keys = self.redis_client.scan(cursor=0, match=match)
        keys.extend(result_keys)
        while (cursor != 0):
            cursor, result_keys = self.redis_client.scan(cursor=cursor, match=match)
            keys.extend(result_keys)
        return keys

    def _serialize_entry(self, entry):
        return jsonpickle.encode(entry)

    def _deserialize_entries(self, serialized_entries):
        return [jsonpickle.decode(serialized_entry) for serialized_entry in serialized_entries]