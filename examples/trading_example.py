"""
Trading API Example
"""
import time
from blofin.client import Client
from blofin.exceptions import BlofinAPIException
from blofin.rest_trading import TradingAPI

def tradingExample():

    # Replace these with your API credentials 
    api_key = "...."
    secret_key = "...."
    passphrase = "...."
    brokerId = "...."  # Your broker ID
    
    client = Client(api_key, secret_key, passphrase)
    trading_api = TradingAPI(client)
    
    print("\n=== Account Information ===")
    # 1. Query API key information
    api_info = trading_api.queryApikey()
    print("API Key Info:", api_info)
    
    # 2. Get account balance
    balance = trading_api.getAccountBalance()
    print("\nAccount Balance:", balance)
    
    print("\n=== Asset Information ===")
    # Get balances for different account types
    for accountType in ("futures","spot", "funding", "earn"):
        assets = trading_api.getBalances(accountType=accountType)
        for asset in assets.get("data", []):
            if float(asset.get('balance')) > 0:
                print(f"\nAccount Assets {accountType}: {asset}")
                
    # Get deposit history
    print("\n=== Deposit History ===")
    deposits = trading_api.getDepositHistory(
        currency="USDT",
        limit="5"  # Get last 5 records
    )
    print("Recent Deposits:", deposits)
    
    # Get withdrawal history
    print("\n=== Withdrawal History ===")
    withdrawals = trading_api.getWithdrawalHistory(
        currency="USDT",
        limit="5"  # Get last 5 records
    )

    
    print("Recent Withdrawals:", withdrawals)
    
    # Get transfer history
    print("\n=== Transfer History ===")
    transfers = trading_api.getBills(
        currency="USDT",
        limit="5"  # Get last 5 records
    )
    print("Recent Transfers:", transfers)
    
    # Transfer funds between accounts
    print("\n=== Transfer Funds ===")
    try:
        transfer = trading_api.transfer(
            currency="USDT",
            amount="1.5",
            fromAccount="funding",
            toAccount="futures",
            clientId=f"test_transfer_{int(time.time())}"
        )
        print("Transfer Result:", transfer)
    except BlofinAPIException as e:
        print("Transfer failed:", e)

    # 3. Cancel all pending orders and set leverage
    print("\n=== Setting Up Trading ===")
    print("Cancelling all pending orders...")
    
    # Cancel normal orders
    pending_orders = trading_api.getOrdersPending(instId="BTC-USDT")
    if pending_orders.get('data'):
        for order in pending_orders.get('data', []):
            order_id = order.get('orderId')
            if order_id:
                result = trading_api.cancelOrder(instId="BTC-USDT", orderId=order_id)
                print(f"Cancelled order {order_id}:", result)
    
    # Cancel TP/SL orders
    pending_tpsl = trading_api.getOrdersTpslPending(instId="BTC-USDT")
    if pending_tpsl.get('data'):
        for order in pending_tpsl.get('data', []):
            tpsl_id = order.get('tpslId')
            if tpsl_id:
                result = trading_api.cancelTpsl([{'tpslId':tpsl_id}])
                print(f"Cancelled TP/SL order {tpsl_id}:", result)
    
    # Cancel algo orders
    pending_algo = trading_api.getOrdersAlgoPending(instId="BTC-USDT")
    if pending_algo.get('data'):
        for order in pending_algo.get('data', []):
            algo_id = order.get('algoId')
            if algo_id:
                result = trading_api.cancelAlgoOrder(instId="BTC-USDT", algoId=algo_id)
                print(f"Cancelled algo order {algo_id}:", result)
    
    # Set leverage
    try:
        leverage = trading_api.setLeverage(
            instId="BTC-USDT",
            leverage="10",  # 10x leverage
            marginMode="cross"
        )
        print("\nLeverage set:", leverage)
    except BlofinAPIException as e:
        print("\nError setting leverage:", e)
    
    # 4. Place orders
    print("\n=== Trading Operations ===")
    # Place a single order
    order = {
        "instId": "BTC-USDT",
        "marginMode": "cross",
        "positionSide": "net",
        "side": "buy",
        "orderType": "limit",
        "size": "0.1",
        "price": "35000",
        "clientOrderId": f"test_{int(time.time())}",
        "brokerId": brokerId
    }
    order_result = trading_api.placeOrder(**order)
    print("\nSingle Order Result:", order_result)
    
    # Place batch orders
    batch_orders = [
        {
            "instId": "BTC-USDT",
            "marginMode": "cross",
            "tradeMode": "cross",
            "side": "buy",
            "orderType": "limit",
            "size": "0.1",
            "price": "34000",
            "clientOrderId": f"test_batch1_{int(time.time())}",
            "brokerId": brokerId
        },
        {
            "instId": "BTC-USDT",
            "marginMode": "cross",
            "tradeMode": "cross",
            "side": "buy",
            "orderType": "limit",
            "size": "0.1",
            "price": "33000",
            "clientOrderId": f"test_batch2_{int(time.time())}",
            "brokerId": brokerId
        }
    ]
    batch_result = trading_api.placeBatchOrders(batch_orders)
    print("\nBatch Orders Result:", batch_result)
    
    # 5. Query orders
    print("\n=== Order Status ===")
    pending = trading_api.getOrdersPending(instId="BTC-USDT")
    print("Pending Orders:", pending)
    
    # 6. Cancel orders
    if pending.get('data'):
        for order in pending.get('data', [])[:1]:  # Cancel the first order
            order_id = order.get('orderId')
            if order_id:
                cancel_result = trading_api.cancelOrder(
                    instId="BTC-USDT",
                    orderId=order_id
                )
                print("\nCancel Order Result:", cancel_result)

    print("\n=== Market Order Example ===")
    # Place a market buy order
    market_order = {
        "instId": "BTC-USDT",
        "marginMode": "cross",
        "positionSide": "net",
        "side": "buy",
        "orderType": "market",
        "size": "0.1",  # Small size for testing
        "clientOrderId": f"test_market_{int(time.time())}",
        "brokerId": brokerId
    }
    market_order_result = trading_api.placeOrder(**market_order)
    print("\nMarket Buy Order Result:", market_order_result)

    # Wait a moment for the order to be filled
    time.sleep(2)

    # Check position
    positions = trading_api.getPositions(instId="BTC-USDT")
    print("\nCurrent Position:", positions)

    if positions.get('data'):
        close_result = trading_api.closePosition(
                        instId="BTC-USDT", 
                        marginMode=positions['data'][0]['marginMode'],
                        positionSide=positions['data'][0]['positionSide'], 
        )
        print("\nPosition Close Result:", close_result)
        # Check final position
        time.sleep(2)
        final_positions = trading_api.getPositions(instId="BTC-USDT")
        print("\nFinal Position:", final_positions)

if __name__ == "__main__":
    tradingExample()  # Uncomment this line after adding your API credentials
