from typing import Dict, Optional
from .client import Client

class MarketAPI:
    """BloFin Market Data REST API client.
    
    Handles all market data related endpoints including instruments, tickers,
    order books, trades, and other market information.
    """
    
    def __init__(self, client: Client):
        self._client = client

    def getInstruments(self, instId: str = None) -> Dict:
        """Get a list of instruments.
        
        Args:
            instId: Optional instrument ID, e.g. BTC-USDT
        
        Returns:
            Dict: Response containing instrument information:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of instruments with details including:
                    - instId: Instrument ID
                    - baseCurrency: Base currency
                    - quoteCurrency: Quote currency
                    - contractValue: Contract value in base currency
                    - listTime: Listing time in milliseconds
                    - expireTime: Instrument offline time
                    - maxLeverage: Maximum leverage
                    - minSize: Minimum order size in contracts
                    - lotSize: Contract size increment
                    - tickSize: Tick size
                    - instType: Instrument type
                    - contractType: Contract type (linear/inverse)
                    - maxLimitSize: Maximum limit order quantity
                    - maxMarketSize: Maximum market order quantity
                    - state: Instrument status (live/suspend)
        """
        params = {}
        if instId:
            params['instId'] = instId
        return self._client.get('/api/v1/market/instruments', params=params, sign=False)

    def getTickers(self, instId: Optional[str] = None) -> Dict:
        """Get latest price snapshot, best bid/ask price, and 24h trading volume.
        
        Args:
            instId: Optional instrument ID to filter results
            
        Returns:
            Dict: Response containing ticker information:
                - last: Latest trade price
                - lastSize: Latest trade size
                - askPrice: Best ask price
                - askSize: Best ask size
                - bidPrice: Best bid price
                - bidSize: Best bid size
                - open24h: Open price in the last 24 hours
                - high24h: Highest price in last 24 hours
                - low24h: Lowest price in last 24 hours
                - volume24h: Trading volume in last 24 hours
                - ts: Timestamp
        """
        params = {}
        if instId:
            params["instId"] = instId
            
        return self._client.get('/api/v1/market/tickers', params=params, sign=False)

    def getOrderBook(self, instId: str, size: Optional[str] = None) -> Dict:
        """Get order book data.
        
        Args:
            instId: Instrument ID
            size: Order book depth per side. Maximum 400, default 1
            
        Returns:
            Dict: Response containing order book data:
                - asks: List of ask orders [price, size]
                - bids: List of bid orders [price, size]
                - ts: Timestamp
        """
        params = {"instId": instId}
        if size:
            params["size"] = size
            
        return self._client.get('/api/v1/market/books', params=params, sign=False)

    def getTrades(self, instId: str, limit: Optional[str] = None) -> Dict:
        """Get recent trades data.
        
        Args:
            instId: Instrument ID
            limit: Number of results per request. Maximum 100, default 100
            
        Returns:
            Dict: Response containing trades data:
                - tradeId: Trade ID
                - price: Trade price
                - size: Trade size
                - side: Trade side (buy/sell)
                - ts: Trade timestamp
        """
        params = {"instId": instId}
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/market/trades', params=params, sign=False)

    def getMarkPrice(self, instId: Optional[str] = None) -> Dict:
        """Get mark price.
        
        Args:
            instId: Optional instrument ID to filter results
            
        Returns:
            Dict: Response containing mark price information:
                - instId: Instrument ID
                - markPrice: Mark price
                - ts: Timestamp
        """
        params = {}
        if instId:
            params["instId"] = instId
            
        return self._client.get('/api/v1/market/mark-price', params=params, sign=False)

    def getFundingRate(self, instId: Optional[str] = None) -> Dict:
        """Get current funding rate.
        
        Args:
            instId: Optional instrument ID to filter results
            
        Returns:
            Dict: Response containing funding rate information:
                - instId: Instrument ID
                - fundingRate: Current funding rate
                - nextFundingRate: Predicted next funding rate
                - fundingTime: Next funding time
        """
        params = {}
        if instId:
            params["instId"] = instId
            
        return self._client.get('/api/v1/market/funding-rate', params=params, sign=False)

    def getFundingRateHistory(
        self,
        instId: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get funding rate history.
        
        Args:
            instId: Instrument ID
            before: Return records newer than this timestamp
            after: Return records older than this timestamp
            limit: Number of results per request. Maximum 100, default 100
            
        Returns:
            Dict: Response containing funding rate history:
                - instId: Instrument ID
                - fundingRate: Funding rate
                - realizedRate: Realized funding rate
                - fundingTime: Funding timestamp
        """
        params = {"instId": instId}
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/market/funding-rate-history', params=params, sign=False)

    def getCandlesticks(
        self,
        instId: str,
        bar: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get candlestick charts data.
        
        Args:
            instId: Instrument ID
            bar: Bar size, default '1m'
                Available values: '1m','3m','5m','15m','30m','1H','2H',
                '4H','6H','8H','12H','1D','3D','1W','1M'
            before: Return records newer than this timestamp
            after: Return records older than this timestamp
            limit: Number of results. Maximum 1440, default 500
            
        Returns:
            Dict: Response containing candlestick data:
                List of [ts, open, high, low, close, vol, volCcy] for each candle
        """
        params = {"instId": instId}
        if bar:
            params["bar"] = bar
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/market/candles', params=params, sign=False)
