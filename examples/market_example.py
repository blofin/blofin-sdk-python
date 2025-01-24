from blofin.client import Client
from blofin.rest_market import MarketAPI

def marketDataExample():
    """Example of using RestMarketAPI to get market data."""
    
    # Initialize client (no authentication needed for public endpoints)
    client = Client()
    marketAPI = MarketAPI(client)
    
    try:
        # 1. Get all instruments
        instruments = marketAPI.getInstruments()
        print("\n=== Instruments ===")
        print(instruments)
        
        # 2. Get ticker for BTC-USDT
        tickers = marketAPI.getTickers(instId="BTC-USDT")
        print("\n=== BTC-USDT Ticker ===")
        print(tickers)
        
        # 3. Get order book for BTC-USDT with depth of 5
        orderBook = marketAPI.getOrderBook(instId="BTC-USDT", size="5")
        print("\n=== BTC-USDT Order Book (Depth: 5) ===")
        print(orderBook)
        
        # 4. Get recent trades for BTC-USDT
        trades = marketAPI.getTrades(instId="BTC-USDT", limit="10")
        print("\n=== BTC-USDT Recent Trades (Last 10) ===")
        print(trades)
        
        # 5. Get mark price for BTC-USDT
        markPrice = marketAPI.getMarkPrice(instId="BTC-USDT")
        print("\n=== BTC-USDT Mark Price ===")
        print(markPrice)
        
        # 6. Get current funding rate for BTC-USDT
        fundingRate = marketAPI.getFundingRate(instId="BTC-USDT")
        print("\n=== BTC-USDT Current Funding Rate ===")
        print(fundingRate)
        
        # 7. Get funding rate history for BTC-USDT
        fundingHistory = marketAPI.getFundingRateHistory(
            instId="BTC-USDT",
            limit="5"  # Get last 5 funding rates
        )
        print("\n=== BTC-USDT Funding Rate History (Last 5) ===")
        print(fundingHistory)
        
        # 8. Get candlestick data for BTC-USDT
        candles = marketAPI.getCandlesticks(
            instId="BTC-USDT",
            bar="15m",  # 15-minute candles
            limit="10"  # Get last 10 candles
        )
        print("\n=== BTC-USDT Candlesticks (15m, Last 10) ===")
        print(candles)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    marketDataExample()
