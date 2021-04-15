import unittest
from hangpy.repositories import ServerRepository


class TestServerRepository(unittest.TestCase):

    def test_instantiate(self):
        server_repository = FakeServerRepository()
        self.assertIsNone(server_repository.get_servers())
        self.assertIsNone(server_repository.add_server(None))
        self.assertIsNone(server_repository.update_server(None))


class FakeServerRepository(ServerRepository):

    def get_servers(self):
        return ServerRepository.get_servers(self)

    def add_server(self, server):
        return ServerRepository.add_server(self, server)

    def update_server(self, server):
        return ServerRepository.update_server(self, server)


if (__name__ == "__main__"):
    unittest.main()
