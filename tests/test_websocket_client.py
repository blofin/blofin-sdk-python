import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import json
from blofin.websocket_client import BlofinWsClient, BlofinWsPublicClient, BlofinWsPrivateClient, BlofinWsCopytradingClient

class TestBlofinWsClient(unittest.TestCase):
    def setUp(self):
        self.apiKey = "test_api_key"
        self.apiSecret = "test_api_secret"
        self.passphrase = "test_passphrase"
        self.client = BlofinWsClient(apiKey=self.apiKey, secret=self.apiSecret, passphrase=self.passphrase)

    def test_init(self):
        """Test WebSocket client initialization"""
        self.assertEqual(self.client.apiKey, self.apiKey)
        self.assertEqual(self.client.secret, self.apiSecret)
        self.assertEqual(self.client.passphrase, self.passphrase)

class TestBlofinWsPublicClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = BlofinWsPublicClient()
        self.mockWs = AsyncMock()
        self.client._ws = self.mockWs
        self.client._connected = True

        # Mock _isConnected method
        self.client._isConnected = MagicMock(return_value=True)

    def test_init(self):
        """Test public WebSocket client initialization"""
        self.assertTrue(self.client.isPublic)

    async def test_subscribeTrades(self):
        """Test subscribing to trades"""
        await self.client.subscribeTrades(instId="BTC-USDT")
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "trades",
                "instId": "BTC-USDT"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribeTickers(self):
        """Test subscribing to tickers"""
        await self.client.subscribeTickers(instId="BTC-USDT")
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "tickers",
                "instId": "BTC-USDT"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

class TestBlofinWsPrivateClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.apiKey = "test_api_key"
        self.apiSecret = "test_api_secret"
        self.passphrase = "test_passphrase"
        self.client = BlofinWsPrivateClient(apiKey=self.apiKey, secret=self.apiSecret, passphrase=self.passphrase)
        self.mockWs = AsyncMock()
        self.client._ws = self.mockWs
        self.client._connected = True

        # Mock _isConnected and _authenticate methods
        self.client._isConnected = MagicMock(return_value=True)
        self.client._authenticate = AsyncMock(return_value=True)

    def test_init(self):
        """Test private WebSocket client initialization"""
        self.assertFalse(self.client.isPublic)
        self.assertEqual(self.client.apiKey, self.apiKey)
        self.assertEqual(self.client.secret, self.apiSecret)
        self.assertEqual(self.client.passphrase, self.passphrase)

    async def test_subscribeOrders(self):
        """Test subscribing to orders"""
        await self.client.subscribeOrders()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "orders"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribePositions(self):
        """Test subscribing to positions"""
        await self.client.subscribePositions()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "positions"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribeAccount(self):
        """Test subscribing to account updates"""
        await self.client.subscribeAccount()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "account"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

class TestBlofinWsCopytradingClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.apiKey = "test_api_key"
        self.apiSecret = "test_api_secret"
        self.passphrase = "test_passphrase"
        self.client = BlofinWsCopytradingClient(apiKey=self.apiKey, secret=self.apiSecret, passphrase=self.passphrase)
        self.mockWs = AsyncMock()
        self.client._ws = self.mockWs
        self.client._connected = True

        # Mock _isConnected and _authenticate methods
        self.client._isConnected = MagicMock(return_value=True)
        self.client._authenticate = AsyncMock(return_value=True)

    def test_init(self):
        """Test copytrading WebSocket client initialization"""
        self.assertFalse(self.client.isPublic)
        self.assertEqual(self.client.apiKey, self.apiKey)
        self.assertEqual(self.client.secret, self.apiSecret)
        self.assertEqual(self.client.passphrase, self.passphrase)

    async def test_subscribeCopytradingPositions(self):
        """Test subscribing to copytrading positions"""
        await self.client.subscribeCopytradingPositions()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "copytrading-positions"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribeCopytradingOrders(self):
        """Test subscribing to copytrading orders"""
        await self.client.subscribeCopytradingOrders()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "copytrading-orders"
            }]
        }
        self.mockWs.send.assert_called_with(json.dumps(expected_message))

if __name__ == '__main__':
    unittest.main()
