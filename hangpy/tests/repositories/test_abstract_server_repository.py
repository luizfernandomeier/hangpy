import unittest
from hangpy.repositories import AbstractServerRepository


class TestAbstractServerRepository(unittest.TestCase):

    def test_instantiate(self):
        server_repository = FakeServerRepository()
        self.assertIsNone(server_repository.get_servers())
        self.assertIsNone(server_repository.add_server(None))
        self.assertIsNone(server_repository.update_server(None))


class FakeServerRepository(AbstractServerRepository):

    def get_servers(self):
        return AbstractServerRepository.get_servers(self)

    def add_server(self, server):
        return AbstractServerRepository.add_server(self, server)

    def update_server(self, server):
        return AbstractServerRepository.update_server(self, server)


if (__name__ == "__main__"):
    unittest.main()
