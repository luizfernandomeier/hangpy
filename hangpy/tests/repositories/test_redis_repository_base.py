import fakeredis
import unittest
from hangpy.repositories import RedisRepositoryBase


def get_redis_repository():
    redis_client = fakeredis.FakeStrictRedis()
    return RedisRepositoryBase(redis_client)


def fill_fake_data(redis_repository):
    [redis_repository.redis_client.set(f'key{index}', f'value{index}') for index in range(20)]


class TestRedisRepositoryBase(unittest.TestCase):

    def setUp(self):
        self.redis_repository = get_redis_repository()

    def test_get_key_with_valid_key(self):
        fill_fake_data(self.redis_repository)
        actual_key = self.redis_repository._get_key('key*').decode()
        self.assertEqual(actual_key, 'key0')

    def test_get_key_with_invalid_key(self):
        fill_fake_data(self.redis_repository)
        actual_key = self.redis_repository._get_key('invalid_key*')
        self.assertIsNone(actual_key)

    def test_get_key_with_no_keys(self):
        actual_key = self.redis_repository._get_key('*')
        self.assertIsNone(actual_key)

    def test_get_keys_with_valid_keys(self):
        fill_fake_data(self.redis_repository)
        actual_keys = sorted([key.decode() for key in self.redis_repository._get_keys('key*')])
        expected_keys = sorted([f'key{index}' for index in range(20)])
        self.assertListEqual(actual_keys, expected_keys)

    def test_get_keys_with_invalid_keys(self):
        fill_fake_data(self.redis_repository)
        actual_keys = [key.decode() for key in self.redis_repository._get_keys('invalid_key*')]
        self.assertListEqual(actual_keys, [])

    def test_get_keys_with_no_keys(self):
        actual_keys = [key.decode() for key in self.redis_repository._get_keys('*')]
        self.assertListEqual(actual_keys, [])

    def test_serialize_entry(self):
        fake_object = FakeClass('luiz', 'fernando')
        actual = self.redis_repository._serialize_entry(fake_object)
        validation_regex = r'\{\"py/object\"\: \".+\.FakeClass\", \"property1\"\: \"luiz\", \"property2\"\: \"fernando\"\}'
        self.assertRegex(actual, validation_regex)

    def test_deserialize_entries(self):
        fake_object = FakeClass('luiz', 'fernando')
        serialized_entry = self.redis_repository._serialize_entry(fake_object)
        actual_objects = self.redis_repository._deserialize_entries([serialized_entry])
        expected_objects = [fake_object]
        self.assertListEqual(actual_objects, expected_objects)

    def test_deserialize_entry(self):
        fake_object = FakeClass('luiz', 'fernando')
        serialized_entry = self.redis_repository._serialize_entry(fake_object)
        actual_object = self.redis_repository._deserialize_entry(serialized_entry)
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
