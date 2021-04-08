import jsonpickle


class RedisRepositoryBase():

    def __init__(self, redis_client):
        self.redis_client = redis_client

    def _get_key(self, match):
        keys = []
        cursor, result_keys = self.redis_client.scan(cursor=0, match=match)
        keys.extend(result_keys)
        while (len(keys) == 0 and cursor != 0):
            cursor, result_keys = self.redis_client.scan(cursor=cursor, match=match)
            keys.extend(result_keys)
        if (len(keys) == 0):
            return None
        return keys[0]

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

    def _deserialize_entry(self, serialized_entry):
        return jsonpickle.decode(serialized_entry)

    def _deserialize_entries(self, serialized_entries):
        return [self._deserialize_entry(serialized_entry) for serialized_entry in serialized_entries]
