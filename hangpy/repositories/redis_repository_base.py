import jsonpickle
from redis import Redis


class RedisRepositoryBase():

    def __init__(self, redis_client: Redis):
        """Base class for the implementations of the Redis repositories.
        It contains common functions used on Redis that don't depend on any
        specific entity.

        Args:
            redis_client (Redis): Implementation of a Redis client.
        """
        self.redis_client = redis_client

    def _get_key(self, match: str) -> str:
        """Returns a key matching the pattern passed by parameter. If no match
        is found, 'None' is returned.

        Args:
            match (str): A string containing a match pattern to filter the
            keys on Redis. This filter uses the same patterns supported by
            native Redis.

        Returns:
            str
        """
        keys = []
        cursor, result_keys = self.redis_client.scan(cursor=0, match=match)
        keys.extend(result_keys)
        while (len(keys) == 0 and cursor != 0):
            cursor, result_keys = self.redis_client.scan(cursor=cursor, match=match)
            keys.extend(result_keys)
        if (len(keys) == 0):
            return None
        return keys[0]

    def _get_keys(self, match: str) -> list[str]:
        """Returns all keys matching the pattern passed by parameter. If no
        match is found, an empty list is returned.

        Args:
            match (str): A string containing a match pattern to filter the
            keys on Redis. This filter uses the same patterns supported by
            native Redis.

        Returns:
            list[str]
        """
        keys = []
        cursor, result_keys = self.redis_client.scan(cursor=0, match=match)
        keys.extend(result_keys)
        while (cursor != 0):
            cursor, result_keys = self.redis_client.scan(cursor=cursor, match=match)
            keys.extend(result_keys)
        return keys

    def _serialize_entry(self, entry: object) -> str:
        """Serializes an object to make it possible to set the record on Redis.
        It uses the 'jsonpickle' serialization package.

        Args:
            entry (object): Any object serializable using 'jsonpickle'.

        Returns:
            str
        """
        return jsonpickle.encode(entry)

    def _deserialize_entry(self, serialized_entry: str) -> object:
        """Deserializes an object using the 'jsonpickle' serialization
        package. It returns an instance of the object.

        Args:
            serialized_entry (str): Any object serialized using 'jsonpickle'.

        Returns:
            object
        """
        return jsonpickle.decode(serialized_entry)

    def _deserialize_entries(self, serialized_entries: list[str]) -> list[object]:
        """Deserializes a list of objects using the 'jsonpickle' serialization
        package. It returns a list of instances of the objects.

        Args:
            serialized_entries (list[str]): A list of any objects serialized
            using 'jsonpickle'.

        Returns:
            list[object]
        """
        return [self._deserialize_entry(serialized_entry) for serialized_entry in serialized_entries]
