import unittest

from app.main import create_app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

    def test_hello(self):
        pass
        # response = self.app.get("/")
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Hello, World!", response.data)

    def test_echo(self):
        pass
        # response = self.app.get("/echo/test")
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b"test", response.data)
