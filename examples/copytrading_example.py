from blofin.client import Client
from blofin.rest_copytrading import CopyTradingAPI
from blofin.rest_market import MarketAPI

def copyTradingExample():
    """Example of using RestCopyTradingAPI for copy trading operations."""
    
    # Replace these with your API credentials
    apiKey = "...."
    secretKey = "...."
    passphrase = "...."
    brokerId = "...."  # Your broker ID
    
    client = Client(apiKey=apiKey, apiSecret=secretKey, passphrase=passphrase)
    copyTradingApi = CopyTradingAPI(client)
    marketApi = MarketAPI(client)
    
    try:
        # 1. Get available instruments
        instruments = copyTradingApi.getInstruments()
        print("\n=== Available Instruments ===")
        print(instruments)
        
        # 2. Get copy trading configuration
        config = copyTradingApi.getConfig()
        print("\n=== Copy Trading Configuration ===")
        print(config)
        
        # 3. Get account balance
        balance = copyTradingApi.getAccountBalance()
        print("\n=== Account Balance ===")
        print(balance)
        
        # Get pending orders first
        pendingOrders = copyTradingApi.getOrdersPending()
        print("\n=== Current Pending Orders ===")
        print(pendingOrders)

        # Cancel all pending orders if any exist
        if pendingOrders['data']:
            for order in pendingOrders['data']:
                cancelResult = copyTradingApi.cancelOrder(
                    orderId=str(order['orderId'])  # Convert to string
                )
                print(f"\n=== Cancel Order Result for {order['orderId']} ===")
                print(cancelResult)

        # Now set position mode and leverage
        positionMode = copyTradingApi.setPositionMode(
            positionMode="net_mode"
        )
        print("\n=== Set Position Mode Result ===")
        print(positionMode)

        leverage = copyTradingApi.setLeverage(
            instId="BTC-USDT",
            leverage="10",
            marginMode="cross",
            positionSide="net"
        )
        print("\n=== Set Leverage Result ===")
        print(leverage)

        # Get current price for reference
        currentPrice = marketApi.getTickers(instId="BTC-USDT")
        print("\n=== Current Price ===")
        print(currentPrice)

        # Place a new order slightly below market price
        lastPrice = float(currentPrice['data'][0]['last'])
        orderPrice = str(round(lastPrice * 1.002, 1))  # 1% below market price

        order = copyTradingApi.placeOrder(
            instId="BTC-USDT",
            marginMode="cross",
            side="buy",
            orderType="limit",
            price=orderPrice,
            size="0.2",
            positionSide="net",
            brokerId=brokerId
        )
        print("\n=== Place Order Result ===")
        print(order)

        # Store orderId for later use
        orderId = order['orderId']
        
        # Check if order is filled
        activeOrders = copyTradingApi.getOrdersPending()
        print("\n=== Order Status ===")
        print(activeOrders)
        
        # Only set TP/SL if order is filled
        isOrderActive = False
        for activeOrder in activeOrders.get('data', []):
            if activeOrder['orderId'] == orderId:
                isOrderActive = True
                break

        if not isOrderActive:  # Order not in active orders means it's filled
            # Place TP/SL orders
            tpPrice = str(round(lastPrice * 1.02, 1))  # 2% profit
            slPrice = str(round(lastPrice * 0.98, 1))  # 2% loss
            
            tpsl = copyTradingApi.placeTpslByOrder(
                orderId=orderId,
                tpTriggerPrice=tpPrice,
                slTriggerPrice=slPrice,
                size="0.1",
                brokerId=brokerId
            )
            print("\n=== Place TP/SL Order Result ===")
            print(tpsl)
        else:
            print("\n=== Order not filled yet, skipping TP/SL ===")
        
        # 8. Get positions by contract
        positions = copyTradingApi.getPositionsByContract(instId="BTC-USDT")
        print("\n=== Current Positions ===")
        print(positions)
        
        # 9. Get pending orders
        pendingOrders = copyTradingApi.getOrdersPending(instId="BTC-USDT")
        print("\n=== Pending Orders ===")
        print(pendingOrders)
        
        # 10. Get pending TP/SL orders by order
        pendingTpsl = copyTradingApi.getPendingTpslByOrder(orderId=orderId)
        print("\n=== Pending TP/SL Orders ===")
        print(pendingTpsl)
        
        # 11. Cancel the order
        cancelResult = copyTradingApi.cancelOrder(
            orderId=orderId
        )
        print("\n=== Cancel Order Result ===")
        print(cancelResult)
        
        closeResult = copyTradingApi.closePositionByOrder(
            orderId=orderId,
            size="0.1",
            brokerId=brokerId
        )
        print("\n=== Close Position By Order Result ===")
        print(closeResult)

        closeResult = copyTradingApi.closePositionByContract(
            instId="BTC-USDT",
            brokerId=brokerId,
            marginMode="cross",
            positionSide="net",
            closeType="fixedRatio",
            size= "1"
        )
        print("\n=== Close Position By Contract Result ===")
        print(closeResult)

        # 12. Get order history
        orderHistory = copyTradingApi.getOrdersHistory(
            instId="BTC-USDT",
            limit="5"  # Get last 5 orders
        )
        print("\n=== Order History ===")
        print(orderHistory)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    copyTradingExample()  # Uncomment this line after adding your API credentials
