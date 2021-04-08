import fakeredis
import unittest
from hangpy.repositories import RedisRepositoryBase


class TestRedisRepositoryBase(unittest.TestCase):

    def test_get_key(self):
        redis_client = fakeredis.FakeStrictRedis()
        [redis_client.set(f'key{index}', f'value{index}') for index in range(20)]
        repository_base = RedisRepositoryBase(redis_client)
        actual_key = repository_base._get_key('key*').decode()
        expected_key = 'key0'
        self.assertEqual(actual_key, expected_key)

        actual_key = repository_base._get_key('invalid_key*')
        self.assertIsNone(actual_key)

        redis_client.flushall()
        actual_key = repository_base._get_key('*')
        self.assertIsNone(actual_key)

    def test_get_keys(self):
        redis_client = fakeredis.FakeStrictRedis()
        [redis_client.set(f'key{index}', f'value{index}') for index in range(20)]
        repository_base = RedisRepositoryBase(redis_client)
        actual_keys = [key.decode() for key in repository_base._get_keys('key*')]
        actual_keys.sort()
        expected_keys = [f'key{index}' for index in range(20)]
        expected_keys.sort()
        self.assertListEqual(actual_keys, expected_keys)

        actual_keys = [key.decode() for key in repository_base._get_keys('invalid_key*')]
        expected_keys = []
        self.assertListEqual(actual_keys, expected_keys)

        redis_client.flushall()
        actual_keys = [key.decode() for key in repository_base._get_keys('*')]
        expected_keys = []
        self.assertListEqual(actual_keys, expected_keys)

    def test_serialize_entry(self):
        redis_client = fakeredis.FakeStrictRedis()
        repository_base = RedisRepositoryBase(redis_client)
        fake_object = FakeClass('luiz', 'fernando')
        actual = repository_base._serialize_entry(fake_object)
        expected_regex = r'\{\"py/object\"\: \".+\.FakeClass\", \"property1\"\: \"luiz\", \"property2\"\: \"fernando\"\}'
        self.assertRegex(actual, expected_regex)

    def test_deserialize_entries(self):
        redis_client = fakeredis.FakeStrictRedis()
        repository_base = RedisRepositoryBase(redis_client)
        fake_object = FakeClass('luiz', 'fernando')
        serialized_entry = repository_base._serialize_entry(fake_object)
        actual_objects = repository_base._deserialize_entries([serialized_entry])
        expected_objects = [fake_object]
        self.assertListEqual(actual_objects, expected_objects)

    def test_deserialize_entry(self):
        redis_client = fakeredis.FakeStrictRedis()
        repository_base = RedisRepositoryBase(redis_client)
        fake_object = FakeClass('luiz', 'fernando')
        serialized_entry = repository_base._serialize_entry(fake_object)
        actual_object = repository_base._deserialize_entry(serialized_entry)
        expected_object = fake_object
        self.assertEqual(actual_object, expected_object)


class FakeClass():

    def __init__(self, property1, property2):
        self.property1 = property1
        self.property2 = property2

    def __eq__(self, other):
        return (isinstance(other, FakeClass)
                and self.property1 == other.property1
                and self.property2 == other.property2)


if (__name__ == "__main__"):
    unittest.main()
