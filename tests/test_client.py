import unittest
from unittest.mock import patch, MagicMock
from blofin.client import Client
from blofin.exceptions import BlofinAPIException

class TestClient(unittest.TestCase):
    def setUp(self):
        self.apiKey = "test_api_key"
        self.apiSecret = "test_api_secret"
        self.client = Client(apiKey=self.apiKey, apiSecret=self.apiSecret)

    def test_init(self):
        """Test client initialization"""
        self.assertEqual(self.client.API_KEY, self.apiKey)
        self.assertEqual(self.client.API_SECRET.decode('utf-8'), self.apiSecret)

if __name__ == '__main__':
    unittest.main()
