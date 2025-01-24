import unittest
from unittest.mock import patch, MagicMock
from blofin.rest_trading import TradingAPI
from blofin.client import Client

class TestRestTradingAPI(unittest.TestCase):
    def setUp(self):
        self.client = Client("test_api_key", "test_api_secret")
        self.trading_api = TradingAPI(self.client)

    def test_init(self):
        """Test RestTradingAPI initialization"""
        self.assertIsInstance(self.trading_api._client, Client)

    def test_get_account_balance(self):
        """Test getAccountBalance method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "totalEquity": "100.00",
                "availableBalance": "90.00"
            }
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getAccountBalance()
            mock_get.assert_called_with('/api/v1/account/balance')
            self.assertEqual(response, mock_response)

    def test_get_balances(self):
        """Test getBalances method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "currency": "USDT",
                "balance": "100.00",
                "available": "90.00",
                "frozen": "10.00"
            }]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getBalances("futures", "USDT")
            mock_get.assert_called_with('/api/v1/asset/balances', params={"accountType": "futures", "currency": "USDT"})
            self.assertEqual(response, mock_response)

    def test_get_bills(self):
        """Test getBills method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "currency": "USDT",
                "amount": "10.00",
                "type": "deposit",
                "timestamp": "1234567890"
            }]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getBills(currency="USDT", limit="100")
            mock_get.assert_called_with('/api/v1/asset/bills', params={"currency": "USDT", "limit": "100"})
            self.assertEqual(response, mock_response)

    def test_get_withdrawal_history(self):
        """Test getWithdrawalHistory method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "currency": "USDT",
                "amount": "10.00",
                "state": "2",
                "timestamp": "1234567890"
            }]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getWithdrawalHistory(currency="USDT", state="2")
            mock_get.assert_called_with('/api/v1/asset/withdrawal-history', params={"currency": "USDT", "state": "2"})
            self.assertEqual(response, mock_response)

    def test_get_deposit_history(self):
        """Test getDepositHistory method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "currency": "USDT",
                "amount": "10.00",
                "state": "2",
                "timestamp": "1234567890"
            }]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getDepositHistory(currency="USDT", state="2")
            mock_get.assert_called_with('/api/v1/asset/deposit-history', params={"currency": "USDT", "state": "2"})
            self.assertEqual(response, mock_response)

    def test_transfer(self):
        """Test transfer method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "transferId": "12345"
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.transfer("USDT", "10.00", "funding", "futures")
            mock_post.assert_called_with('/api/v1/asset/transfer', {
                "currency": "USDT",
                "amount": "10.00",
                "fromAccount": "funding",
                "toAccount": "futures"
            })
            self.assertEqual(response, mock_response)

    def test_get_positions(self):
        """Test getPositions method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "instId": "BTC-USDT",
                "posId": "12345",
                "pos": "1",
                "posSide": "long"
            }]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getPositions("BTC-USDT")
            mock_get.assert_called_with('/api/v1/account/positions', params={"instId": "BTC-USDT"})
            self.assertEqual(response, mock_response)

    def test_get_margin_mode(self):
        """Test getMarginMode method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "marginMode": "cross"
            }
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getMarginMode()
            mock_get.assert_called_with('/api/v1/account/margin-mode')
            self.assertEqual(response, mock_response)

    def test_get_position_mode(self):
        """Test getPositionMode method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "positionMode": "long_short_mode"
            }
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getPositionMode()
            mock_get.assert_called_with('/api/v1/account/position-mode')
            self.assertEqual(response, mock_response)

    def test_get_leverage_info(self):
        """Test getLeverageInfo method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "leverage": "20",
                "maxLeverage": "100"
            }
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getLeverageInfo("BTC-USDT", "cross")
            mock_get.assert_called_with('/api/v1/account/leverage-info', params={"instId": "BTC-USDT", "marginMode": "cross"})
            self.assertEqual(response, mock_response)

    def test_get_batch_leverage_info(self):
        """Test getBatchLeverageInfo method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "instId": "BTC-USDT",
                "leverage": "20",
                "maxLeverage": "100"
            }]
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.trading_api.getBatchLeverageInfo(["BTC-USDT", "ETH-USDT"], "cross")
            mock_get.assert_called_with('/api/v1/account/batch-leverage-info', params={"instId": "BTC-USDT,ETH-USDT", "marginMode": "cross"})
            self.assertEqual(response, mock_response)

    def test_place_order(self):
        """Test placeOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "orderId": "12345",
                "clientOrderId": "test123",
                "code": "0",
                "msg": ""
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.placeOrder(
                instId="BTC-USDT",
                marginMode="cross",
                positionSide="net",
                side="buy",
                orderType="limit",
                price="20000",
                size="0.01"
            )
            mock_post.assert_called_with('/api/v1/trade/order', {
                "instId": "BTC-USDT",
                "marginMode": "cross",
                "positionSide": "net",
                "side": "buy",
                "orderType": "limit",
                "price": "20000",
                "size": "0.01"
            })
            self.assertEqual(response, mock_response)

    def test_place_batch_orders(self):
        """Test placeBatchOrders method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "orderId": "12345",
                "clientOrderId": "test123",
                "code": "0",
                "msg": ""
            }]
        }
        orders = [{
            "instId": "BTC-USDT",
            "marginMode": "cross",
            "positionSide": "net",
            "side": "buy",
            "orderType": "limit",
            "price": "20000",
            "size": "0.01"
        }]
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.placeBatchOrders(orders)
            mock_post.assert_called_with('/api/v1/trade/batch-orders', orders)
            self.assertEqual(response, mock_response)

    def test_place_tpsl(self):
        """Test placeTpsl method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "tpslId": "1012",
                "clientOrderId": None,
                "code": "0",
                "msg": None
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.placeTpsl(
                instId="ETH-USDT",
                marginMode="cross",
                positionSide="short",
                side="sell",
                size="1",
                tpTriggerPrice="1661.1",
                tpOrderPrice="-1"
            )
            mock_post.assert_called_with('/api/v1/trade/order-tpsl', {
                "instId": "ETH-USDT",
                "marginMode": "cross",
                "positionSide": "short",
                "side": "sell",
                "size": "1",
                "tpTriggerPrice": "1661.1",
                "tpOrderPrice": "-1"
            })
            self.assertEqual(response, mock_response)

    def test_place_algo_order(self):
        """Test placeAlgoOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "algoId": "1012",
                "clientOrderId": None,
                "code": "0",
                "msg": None
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.placeAlgoOrder(
                instId="ETH-USDT",
                marginMode="cross",
                positionSide="short",
                side="sell",
                size="1",
                orderType="trigger",
                triggerPrice="3000",
                orderPrice="-1",
                triggerPriceType="last",
                attachAlgoOrders=[{
                    "tpTriggerPrice": "3500",
                    "tpOrderPrice": "3600",
                    "tpTriggerPriceType": "last",
                    "slTriggerPrice": "2600",
                    "slOrderPrice": "2500",
                    "slTriggerPriceType": "last"
                }]
            )
            mock_post.assert_called_with('/api/v1/trade/order-algo', {
                "instId": "ETH-USDT",
                "marginMode": "cross",
                "positionSide": "short",
                "side": "sell",
                "size": "1",
                "orderType": "trigger",
                "triggerPrice": "3000",
                "orderPrice": "-1",
                "triggerPriceType": "last",
                "attachAlgoOrders": [{
                    "tpTriggerPrice": "3500",
                    "tpOrderPrice": "3600",
                    "tpTriggerPriceType": "last",
                    "slTriggerPrice": "2600",
                    "slOrderPrice": "2500",
                    "slTriggerPriceType": "last"
                }]
            })
            self.assertEqual(response, mock_response)

    def test_cancel_order(self):
        """Test cancelOrder method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "orderId": "12345"
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.cancelOrder("12345")
            mock_post.assert_called_with('/api/v1/trade/cancel-order', {
                "orderId": "12345"
            })
            self.assertEqual(response, mock_response)

    def test_cancel_batch_orders(self):
        """Test cancelBatchOrders method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "orderId": "12345"
            }]
        }
        orders = [{
            "instId": "BTC-USDT",
            "orderId": "12345"
        }]
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.cancelBatchOrders(orders)
            mock_post.assert_called_with('/api/v1/trade/cancel-batch-orders', orders)
            self.assertEqual(response, mock_response)

    def test_close_position(self):
        """Test closePosition method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "orderId": "12345"
            }
        }
        with patch.object(self.client, 'post', return_value=mock_response) as mock_post:
            response = self.trading_api.closePosition("BTC-USDT", "cross", "long")
            mock_post.assert_called_with('/api/v1/trade/close-position', {
                "instId": "BTC-USDT",
                "marginMode": "cross",
                "positionSide": "long",
            })
            self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
