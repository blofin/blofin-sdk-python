import unittest
from unittest.mock import patch, MagicMock
from blofin.rest_affiliate import AffiliateAPI
from blofin.client import Client
from typing import Dict

class TestRestAffiliateAPI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.client = Client("test_api_key", "test_api_secret", "test_passphrase")
        self.affiliate_api = AffiliateAPI(self.client)

    def test_init(self):
        """Test AffiliateAPI initialization"""
        self.assertIsInstance(self.affiliate_api._client, Client)

    def test_get_basic_info(self):
        """Test getBasicInfo method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": {
                "commissionRate": "0.4",
                "cashbackRate": "0.05",
                "totalCommission": "0.0217",
                "referralCode": "my5rDC",
                "referralLink": "https://example.com",
                "directInvitees": "3",
                "subInvitees": "5",
                "tradeInvitees": "2",
                "updateTime": "1737630618520"
            }
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.affiliate_api.getBasicInfo()
            mock_get.assert_called_with('/api/v1/affiliate/basic')
            self.assertEqual(response, mock_response)

    def test_get_invitees(self):
        """Test getInvitees method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "id": 454374,
                "uid": "13227654351",
                "registerTime": "1737547079902",
                "totalTradingVolume": "105.7028",
                "totalTradingFee": "0.0586",
                "totalCommission": "0.0217",
                "totalDeposit": "10",
                "totalWithdrawal": "0",
                "kycLevel": "0",
                "equity": "9.876188266"
            }]
        }
        params = {
            "uid": "13227654351",
            "begin": "1737547079902",
            "end": "1737630618520",
            "limit": "10"
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.affiliate_api.getInvitees(**params)
            mock_get.assert_called_with('/api/v1/affiliate/invitees', params)
            self.assertEqual(response, mock_response)

    def test_get_sub_invitees(self):
        """Test getSubInvitees method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": []
        }
        params = {
            "subAffiliateUid": "30285102093",
            "subAffiliateLevel": "2",
            "begin": "1737547079902",
            "limit": "10"
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.affiliate_api.getSubInvitees(**params)
            mock_get.assert_called_with('/api/v1/affiliate/sub-invitees', params={'subAffiliateUid': '30285102093', 'subAffiliateLevel': '2', 'begin': '1737547079902', 'limit': '10'})
            self.assertEqual(response, mock_response)

    def test_get_sub_affiliates(self):
        """Test getSubAffiliates method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": []
        }
        params = {
            "subAffiliateLevel": "2",
            "begin": "1737547079902",
            "limit": "10"
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.affiliate_api.getSubAffiliates(**params)
            mock_get.assert_called_with('/api/v1/affiliate/sub-affiliates', params)
            self.assertEqual(response, mock_response)

    def test_get_invitees_daily_commission(self):
        """Test getInviteesDailyCommission method"""
        mock_response = {
            "code": "0",
            "msg": "success",
            "data": [{
                "id": "9999",
                "uid": "30292758476",
                "commission": "0.032035434",
                "commissionTime": "1716912000000",
                "cashback": "0.288318906",
                "fee": "3.2035434",
                "kycLevel": "0"
            }]
        }
        params = {
            "uid": "30292758476",
            "begin": "1737547079902",
            "limit": "30"
        }
        with patch.object(self.client, 'get', return_value=mock_response) as mock_get:
            response = self.affiliate_api.getInviteesDailyCommission(**params)
            mock_get.assert_called_with('/api/v1/affiliate/invitees/daily', params)
            self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
