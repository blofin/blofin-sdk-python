from blofin.client import Client
from blofin.rest_copytrading import CopyTradingAPI
from blofin.rest_market import MarketAPI
import time

def copytrading_example():
    """Example of using RestCopyTradingAPI for copy trading operations."""
    
    # Replace these with your API credentials
    api_key = "...."
    secret_key = "...."
    passphrase = "...."
    brokerId = "...."  # Your broker ID
    
    client = Client(api_key=api_key, api_secret=secret_key, passphrase=passphrase)
    copytrading_api = CopyTradingAPI(client)
    market_api = MarketAPI(client)
    
    try:
        # 1. Get available instruments
        instruments = copytrading_api.getInstruments()
        print("\n=== Available Instruments ===")
        print(instruments)
        
        # 2. Get copy trading configuration
        config = copytrading_api.getConfig()
        print("\n=== Copy Trading Configuration ===")
        print(config)
        
        # 3. Get account balance
        balance = copytrading_api.getAccountBalance()
        print("\n=== Account Balance ===")
        print(balance)
        
        # Get pending orders first
        pending_orders = copytrading_api.getOrdersPending()
        print("\n=== Current Pending Orders ===")
        print(pending_orders)

        # Cancel all pending orders if any exist
        if pending_orders['data']:
            for order in pending_orders['data']:
                cancel_result = copytrading_api.cancelOrder(
                    orderId=str(order['orderId'])  # Convert to string
                )
                print(f"\n=== Cancel Order Result for {order['orderId']} ===")
                print(cancel_result)

        # Now set position mode and leverage
        position_mode = copytrading_api.setPositionMode(
            positionMode="net_mode"
        )
        print("\n=== Set Position Mode Result ===")
        print(position_mode)

        leverage = copytrading_api.setLeverage(
            instId="BTC-USDT",
            leverage="10",
            marginMode="cross",
            positionSide="net"
        )
        print("\n=== Set Leverage Result ===")
        print(leverage)

        # Get current price for reference
        current_price = market_api.getTickers(instId="BTC-USDT")
        print("\n=== Current Price ===")
        print(current_price)

        # Place a new order slightly below market price
        last_price = float(current_price['data'][0]['last'])
        order_price = str(round(last_price * 1.002, 1))  # 1% below market price

        order = copytrading_api.placeOrder(
            instId="BTC-USDT",
            marginMode="cross",
            side="buy",
            orderType="limit",
            price=order_price,
            size="0.2",
            positionSide="net",
            brokerId=brokerId
        )
        print("\n=== Place Order Result ===")
        print(order)

        # Store orderId for later use
        order_id = order['orderId']
        
        # Check if order is filled
        active_orders = copytrading_api.getOrdersPending()
        print("\n=== Order Status ===")
        print(active_orders)
        
        # Only set TP/SL if order is filled
        is_order_active = False
        for active_order in active_orders.get('data', []):
            if active_order['orderId'] == order_id:
                is_order_active = True
                break

        if not is_order_active:  # Order not in active orders means it's filled
            # Place TP/SL orders
            tp_price = str(round(last_price * 1.02, 1))  # 2% profit
            sl_price = str(round(last_price * 0.98, 1))  # 2% loss
            
            tpsl = copytrading_api.placeTpslByOrder(
                orderId=order_id,
                tpTriggerPrice=tp_price,
                slTriggerPrice=sl_price,
                size="0.1",
                brokerId=brokerId
            )
            print("\n=== Place TP/SL Order Result ===")
            print(tpsl)
        else:
            print("\n=== Order not filled yet, skipping TP/SL ===")
        
        # 8. Get positions by contract
        positions = copytrading_api.getPositionsByContract(instId="BTC-USDT")
        print("\n=== Current Positions ===")
        print(positions)
        
        # 9. Get pending orders
        pending_orders = copytrading_api.getOrdersPending(instId="BTC-USDT")
        print("\n=== Pending Orders ===")
        print(pending_orders)
        
        # 10. Get pending TP/SL orders by order
        pending_tpsl = copytrading_api.getPendingTpslByOrder(orderId=order_id)
        print("\n=== Pending TP/SL Orders ===")
        print(pending_tpsl)
        
        # 11. Cancel the order
        cancel_result = copytrading_api.cancelOrder(
            orderId=order_id
        )
        print("\n=== Cancel Order Result ===")
        print(cancel_result)
        
        close_result = copytrading_api.closePositionByOrder(
            orderId=order_id,
            size="0.1",
            brokerId=brokerId
        )
        print("\n=== Close Position By Order Result ===")
        print(close_result)

        close_result = copytrading_api.closePositionByContract(
            instId="BTC-USDT",
            brokerId=brokerId,
            marginMode="cross",
            positionSide="net",
            closeType="fixedRatio",
            size= "1"
        )
        print("\n=== Close Position By Contract Result ===")
        print(close_result)

        # 12. Get order history
        order_history = copytrading_api.getOrdersHistory(
            instId="BTC-USDT",
            limit="5"  # Get last 5 orders
        )
        print("\n=== Order History ===")
        print(order_history)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    copytrading_example()  # Uncomment this line after adding your API credentials
