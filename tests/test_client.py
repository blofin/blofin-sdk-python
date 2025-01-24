import unittest
from unittest.mock import patch, MagicMock
from blofin.client import Client
from blofin.exceptions import BlofinAPIException

class TestClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.client = Client(self.api_key, self.api_secret)

    def test_init(self):
        """Test client initialization"""
        self.assertEqual(self.client.API_KEY, self.api_key)
        self.assertEqual(self.client.API_SECRET.decode('utf-8'), self.api_secret)

if __name__ == '__main__':
    unittest.main()
