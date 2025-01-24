import unittest
from unittest.mock import patch, MagicMock
from blofin.rest_copytrading import CopyTradingAPI
from blofin.client import Client

class TestRestCopyTradingAPI(unittest.TestCase):
    def setUp(self):
        self.client = Client("test_api_key", "test_api_secret")
        self.copytrading_api = CopyTradingAPI(self.client)

    def test_init(self):
        """Test RestCopyTradingAPI initialization"""
        self.assertIsInstance(self.copytrading_api._client, Client)

    def test_get_instruments(self):
        """Test getInstruments method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": ["BTC-USDT", "ETH-USDT"]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.copytrading_api.getInstruments()
            mock_get.assert_called_with('/api/v1/copytrading/instruments')
            self.assertEqual(response, mock_response)

    def test_get_config(self):
        """Test getConfig method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {"roleType": 1}
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.copytrading_api.getConfig()
            mock_get.assert_called_with('/api/v1/copytrading/config')
            self.assertEqual(response, mock_response)

    def test_get_account_balance(self):
        """Test getAccountBalance method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "totalEquity": "1000.00",
                "isolatedEquity": "0.00"
            }
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.copytrading_api.getAccountBalance()
            mock_get.assert_called_with('/api/v1/copytrading/account/balance')
            self.assertEqual(response, mock_response)

    def test_place_order(self):
        """Test placeOrder method"""
        mock_response = {
            "code": "0",
            "msg": "",
            "data": [{
                "orderId": "28150801",
                "clientOrderId": "test1597321",
                "msg": "",
                "code": "0"
            }]
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.placeOrder(
                instId="BTC-USDT",
                marginMode="cross",
                positionSide="net",
                side="buy",
                orderType="limit",
                price="23212.2",
                size="2"
            )
            mock_post.assert_called_with('/api/v1/copytrading/trade/place-order', {
                "instId": "BTC-USDT",
                "marginMode": "cross",
                "positionSide": "net",
                "side": "buy",
                "orderType": "limit",
                "price": "23212.2",
                "size": "2"
            })
            self.assertEqual(response, mock_response)

    def test_cancel_order(self):
        """Test cancelOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "code": "0",
                "msg": None
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.cancelOrder(orderId="123456")
            mock_post.assert_called_with('/api/v1/copytrading/trade/cancel-order', {
                'orderId': '123456'
            })
            self.assertEqual(response, mock_response)

    def test_close_position_by_contract(self):
        """Test closePositionByContract method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {}
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.closePositionByContract(
                instId="BTC-USDT",
                size="0.1",
                marginMode="cross",
                positionSide="net",
                closeType="fixedRatio",
                brokerId="test_broker"
            )
            mock_post.assert_called_with('/api/v1/copytrading/trade/close-position-by-contract', {
                'instId': 'BTC-USDT',
                'size': '0.1',
                'marginMode': 'cross',
                'positionSide': 'net',
                'closeType': 'fixedRatio',
                'brokerId': 'test_broker'
            })
            self.assertEqual(response, mock_response)

    def test_close_position_by_order(self):
        """Test closePositionByOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success"
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.closePositionByOrder(
                orderId="123456",
                size="0.1",
                brokerId="test_broker"
            )
            mock_post.assert_called_with('/api/v1/copytrading/trade/close-position-by-order', {
                'orderId': '123456',
                'size': '0.1',
                'brokerId': 'test_broker'
            })
            self.assertEqual(response, mock_response)

    def test_place_tpsl_by_contract(self):
        """Test placeTpslByContract method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "algoId": "1234543265637"
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.placeTpslByContract(
                instId="BTC-USDT",
                marginMode="cross",
                positionSide="short",
                tpTriggerPrice="80000",
                slTriggerPrice="101000",
                size="-1"
            )
            mock_post.assert_called_with('/api/v1/copytrading/trade/place-tpsl-by-contract', {
                "instId": "BTC-USDT",
                "marginMode": "cross",
                "positionSide": "short",
                "tpTriggerPrice": "80000",
                "slTriggerPrice": "101000",
                "size": "-1"
            })
            self.assertEqual(response, mock_response)

    def test_place_tpsl_by_order(self):
        """Test placeTpslByOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success"
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.placeTpslByOrder(
                orderId="23209016",
                tpTriggerPrice="80000",
                slTriggerPrice="70000",
                size="-1"
            )
            mock_post.assert_called_with('/api/v1/copytrading/trade/place-tpsl-by-order', {
                "orderId": "23209016",
                "tpTriggerPrice": "80000",
                "slTriggerPrice": "70000",
                "size": "-1"
            })
            self.assertEqual(response, mock_response)

    def test_cancel_tpsl_by_contract(self):
        """Test cancelTpslByContract method"""
        mock_response = {
            "code": "0",
            "msg": "success"
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.cancelTpslByContract(algoId="23209016")
            mock_post.assert_called_with('/api/v1/copytrading/trade/cancel-tpsl-by-contract', {
                'algoId': '23209016'
            })
            self.assertEqual(response, mock_response)

    def test_cancel_tpsl_by_order(self):
        """Test cancelTpslByOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success"
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.copytrading_api.cancelTpslByOrder(orderId="23209016")
            mock_post.assert_called_with('/api/v1/copytrading/trade/cancel-tpsl-by-order', {
                'orderId': '23209016'
            })
            self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
