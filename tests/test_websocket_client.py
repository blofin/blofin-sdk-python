import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import json
from blofin.websocket_client import BlofinWsClient, BlofinWsPublicClient, BlofinWsPrivateClient, BlofinWsCopytradingClient

class TestBlofinWsClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.passphrase = "test_passphrase"
        self.client = BlofinWsClient(apiKey=self.api_key, secret=self.api_secret, passphrase=self.passphrase)

    def test_init(self):
        """Test WebSocket client initialization"""
        self.assertEqual(self.client.apiKey, self.api_key)
        self.assertEqual(self.client.secret, self.api_secret)
        self.assertEqual(self.client.passphrase, self.passphrase)

class TestBlofinWsPublicClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = BlofinWsPublicClient()
        self.mock_ws = AsyncMock()
        self.client._ws = self.mock_ws
        self.client._connected = True

        # Mock _isConnected method
        self.client._isConnected = MagicMock(return_value=True)

    def test_init(self):
        """Test public WebSocket client initialization"""
        self.assertTrue(self.client.isPublic)

    async def test_subscribe_trades(self):
        """Test subscribing to trades"""
        await self.client.subscribeTrades("BTC-USDT")
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "trades",
                "instId": "BTC-USDT"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribe_tickers(self):
        """Test subscribing to tickers"""
        await self.client.subscribeTickers("BTC-USDT")
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "tickers",
                "instId": "BTC-USDT"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

class TestBlofinWsPrivateClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.passphrase = "test_passphrase"
        self.client = BlofinWsPrivateClient(self.api_key, self.api_secret, self.passphrase)
        self.mock_ws = AsyncMock()
        self.client._ws = self.mock_ws
        self.client._connected = True

        # Mock _isConnected and _authenticate methods
        self.client._isConnected = MagicMock(return_value=True)
        self.client._authenticate = AsyncMock(return_value=True)

    def test_init(self):
        """Test private WebSocket client initialization"""
        self.assertFalse(self.client.isPublic)
        self.assertEqual(self.client.apiKey, self.api_key)
        self.assertEqual(self.client.secret, self.api_secret)
        self.assertEqual(self.client.passphrase, self.passphrase)

    async def test_subscribe_orders(self):
        """Test subscribing to orders"""
        await self.client.subscribeOrders()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "orders"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribe_positions(self):
        """Test subscribing to positions"""
        await self.client.subscribePositions()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "positions"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribe_account(self):
        """Test subscribing to account updates"""
        await self.client.subscribeAccount()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "account"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

class TestBlofinWsCopytradingClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        self.passphrase = "test_passphrase"
        self.client = BlofinWsCopytradingClient(self.api_key, self.api_secret, self.passphrase)
        self.mock_ws = AsyncMock()
        self.client._ws = self.mock_ws
        self.client._connected = True

        # Mock _isConnected and _authenticate methods
        self.client._isConnected = MagicMock(return_value=True)
        self.client._authenticate = AsyncMock(return_value=True)

    def test_init(self):
        """Test copytrading WebSocket client initialization"""
        self.assertFalse(self.client.isPublic)
        self.assertEqual(self.client.apiKey, self.api_key)
        self.assertEqual(self.client.secret, self.api_secret)
        self.assertEqual(self.client.passphrase, self.passphrase)

    async def test_subscribe_copytrading_positions(self):
        """Test subscribing to copytrading positions"""
        await self.client.subscribeCopytradingPositions()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "copytrading-positions"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

    async def test_subscribe_copytrading_orders(self):
        """Test subscribing to copytrading orders"""
        await self.client.subscribeCopytradingOrders()
        
        expected_message = {
            "op": "subscribe",
            "args": [{
                "channel": "copytrading-orders"
            }]
        }
        self.mock_ws.send.assert_called_with(json.dumps(expected_message))

if __name__ == '__main__':
    unittest.main()
