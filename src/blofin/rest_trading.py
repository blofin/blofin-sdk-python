from typing import Dict, Optional, List
from .client import Client

class TradingAPI:
    """BloFin Trading REST API client.
    
    Handles trading operations, account management, and asset operations.
    """
    
    def __init__(self, client: Client):
        self._client = client

    # Asset endpoints
    def getBalances(
        self,
        accountType: str,
        currency: Optional[str] = None
    ) -> Dict:
        """Get asset balances.
        
        Args:
            accountType: Account type, one of: funding/futures/copy_trading/earn/spot
            currency: Optional, filter by currency
            
        Returns:
            Dict: Response containing balance information for the specified account type
        """
        params = {"accountType": accountType}
        if currency:
            params["currency"] = currency
            
        return self._client.get('/api/v1/asset/balances', params=params)

    def getBills(
        self,
        currency: Optional[str] = None,
        fromAccount: Optional[str] = None,
        toAccount: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get funds transfer history.
        
        Args:
            currency: Filter by currency, e.g. USDT
            fromAccount: The remitting account (funding/futures/copy_trading/earn/spot)
            toAccount: The beneficiary account (funding/futures/copy_trading/earn/spot)
            before: Return records newer than this timestamp (Unix timestamp in milliseconds)
            after: Return records older than this timestamp (Unix timestamp in milliseconds)
            limit: Number of results per request, max 100, default 100
            
        Returns:
            Dict: Response containing transfer history records
        """
        params = {}
        if currency:
            params["currency"] = currency
        if fromAccount:
            params["fromAccount"] = fromAccount
        if toAccount:
            params["toAccount"] = toAccount
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/asset/bills', params=params)

    def getWithdrawalHistory(
        self,
        currency: Optional[str] = None,
        withdrawId: Optional[str] = None,
        txId: Optional[str] = None,
        state: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get withdrawal history.
        
        Args:
            currency: Optional, filter by currency, e.g. USDT
            withdrawId: Optional, filter by withdrawal ID
            txId: Optional, filter by transaction hash
            state: Optional, filter by withdrawal status:
                   - 0: waiting mannual review
                   - 2: failed
                   - 3: success
                   - 4: canceled
                   - 6: kyt
                   - 7: processing
            before: Optional, pagination of data to return records newer than the requested ts,
                   Unix timestamp format in milliseconds, e.g. 1656633600000
            after: Optional, pagination of data to return records earlier than the requested ts,
                   Unix timestamp format in milliseconds, e.g. 1654041600000
            limit: Optional, number of results per request.
                  Maximum is 100, default is 20
            
        Returns:
            Dict: Response containing withdrawal history:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of withdrawal records, each containing:
                    - currency: Withdraw currency
                    - chain: Chain name, e.g. ERC20, TRC20
                    - address: Receiving address
                    - type: Withdraw type (0: blockchain withdraw, 1: internal transfers)
                    - txId: Hash record of the withdrawal
                    - amount: Withdrawal amount
                    - fee: Withdrawal fee amount
                    - feeCurrency: Withdrawal fee currency, e.g. USDT
                    - state: Status of withdrawal (see state parameter description)
                    - clientId: Client-supplied ID
                    - ts: Time the withdrawal request was submitted (milliseconds)
                    - tag: Optional tag for specific currencies
                    - memo: Optional memo for specific currencies
                    - withdrawId: Withdrawal ID
        """
        params = {}
        if currency:
            params["currency"] = currency
        if withdrawId:
            params["withdrawId"] = withdrawId
        if txId:
            params["txId"] = txId
        if state:
            params["state"] = state
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/asset/withdrawal-history', params=params)

    def getDepositHistory(
        self,
        currency: Optional[str] = None,
        depositId: Optional[str] = None,
        txId: Optional[str] = None,
        state: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get deposit history.
        
        Args:
            currency: Optional, filter by currency, e.g. USDT
            depositId: Optional, filter by deposit ID
            txId: Optional, filter by transaction hash
            state: Optional, filter by state:
                   - 0: pending
                   - 1: done
                   - 2: failed
                   - 3: kyt
            before: Optional, pagination of data to return records newer than the requested ts,
                   Unix timestamp format in milliseconds, e.g. 1656633600000
            after: Optional, pagination of data to return records earlier than the requested ts,
                   Unix timestamp format in milliseconds, e.g. 1654041600000
            limit: Optional, number of results per request.
                  Maximum is 100, default is 20
            
        Returns:
            Dict: Response containing deposit history:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of deposit records, each containing:
                    - currency: Currency
                    - chain: Chain name, e.g. ERC20, TRC20
                    - address: Deposit address
                    - type: Deposit type (0: blockchain deposit, 1: internal transfers)
                    - txId: Hash record of the deposit
                    - amount: Deposit amount
                    - state: Status of deposit (0: pending, 1: done, 2: failed, 3: kyt)
                    - confirm: Number of confirmations
                    - ts: Time the deposit request was submitted (milliseconds)
                    - depositId: Deposit ID
        """
        params = {}
        if currency:
            params["currency"] = currency
        if depositId:
            params["depositId"] = depositId
        if txId:
            params["txId"] = txId
        if state:
            params["state"] = state
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/asset/deposit-history', params=params)

    def transfer(
        self,
        currency: str,
        amount: str,
        fromAccount: str,
        toAccount: str,
        clientId: Optional[str] = None
    ) -> Dict:
        """Transfer funds between accounts.
        
        Args:
            currency: Transfer currency, e.g. USDT
            amount: Amount to be transferred
            fromAccount: The remitting account (funding/futures/copy_trading/earn/spot)
            toAccount: The beneficiary account (funding/futures/copy_trading/earn/spot)
            clientId: Optional, client-supplied ID (up to 32 alphanumeric characters)
            
        Returns:
            Dict: Response containing transfer result with transferId
        """
        data = {
            "currency": currency,
            "amount": amount,
            "fromAccount": fromAccount,
            "toAccount": toAccount
        }
        if clientId:
            data["clientId"] = clientId
            
        return self._client.post('/api/v1/asset/transfer', data)

    # Account endpoints
    def getAccountBalance(self) -> Dict:
        """Get account balance.
        
        Returns:
            Dict: Response containing account balance
        """
        return self._client.get('/api/v1/account/balance')

    def getPositions(
        self,
        instId: Optional[str] = None
    ) -> Dict:
        """Get positions.
        
        Args:
            instId: Optional, Filter by instrument ID, e.g. BTC-USDT
            
        Returns:
            Dict: Response containing position information:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of positions, each containing:
                    - positionId: Position ID
                    - instId: Instrument ID
                    - instType: Instrument type
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side (long/short/net)
                    - leverage: Leverage
                    - positions: Quantity of positions
                    - availablePositions: Position that can be closed
                    - averagePrice: Average open price
                    - markPrice: Latest Mark price
                    - marginRatio: Margin ratio
                    - liquidationPrice: Estimated liquidation price
                    - unrealizedPnl: Unrealized profit and loss
                    - unrealizedPnlRatio: Unrealized profit and loss ratio
                    - initialMargin: Initial margin requirement (cross only)
                    - maintenanceMargin: Maintenance margin requirement
                    - createTime: Creation time in milliseconds
                    - updateTime: Last adjustment time in milliseconds
                    
        Note:
            For positionSide:
            - In long/short mode: positions is always positive
            - In net mode: positive positions means long position,
              negative positions means short position
            
        Examples:
            >>> # Get all positions
            >>> api.getPositions()
            
            >>> # Get positions for specific instrument
            >>> api.getPositions(instId="BTC-USDT")
        """
        params = {}
        if instId:
            params["instId"] = instId
            
        return self._client.get('/api/v1/account/positions', params=params)

    def getMarginMode(self) -> Dict:
        """Get margin mode setting.
        
        Returns:
            Dict: Response containing margin mode information
        """
        return self._client.get('/api/v1/account/margin-mode')

    def getPositionMode(self) -> Dict:
        """Get position mode setting.
        
        Returns:
            Dict: Response containing position mode information
        """
        return self._client.get('/api/v1/account/position-mode')

    def getLeverageInfo(self, instId: str, marginMode: str) -> Dict:
        """Get leverage information.
        
        Args:
            instId: Instrument ID
            marginMode: Margin mode (cross/isolated)
            
        Returns:
            Dict: Response containing leverage information
        """
        params = {
            "instId": instId,
            "marginMode": marginMode
        }
        return self._client.get('/api/v1/account/leverage-info', params=params)

    def getBatchLeverageInfo(self, instIds: List[str], marginMode: str) -> Dict:
        """Get leverage information for multiple instruments.
        
        Args:
            instIds: List of instrument IDs (max 20 instruments)
            marginMode: Margin mode (cross/isolated)
            
        Returns:
            Dict: Response containing leverage information including leverage, marginMode, instId and positionSide
        """
        params = {
            "instId": ",".join(instIds),
            "marginMode": marginMode
        }
        return self._client.get('/api/v1/account/batch-leverage-info', params=params)

    # Trading endpoints
    def getOrdersPending(
        self,
        instId: Optional[str] = None,
        orderType: Optional[str] = None,
        state: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get pending orders.
        
        Args:
            instId: Filter by instrument ID
            orderType: Order type (market, limit, post_only, fok, ioc)
            state: Order state (live, partially_filled)
            before: Return records newer than this order ID
            after: Return records older than this order ID
            limit: Number of results per request. Max 100, default 20
            
        Returns:
            Dict: Response containing pending orders
            
        Note:
            The before and after parameters cannot be used simultaneously.
        """
        params = {}
        if instId:
            params["instId"] = instId
        if orderType:
            params["orderType"] = orderType
        if state:
            params["state"] = state
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/orders-pending', params=params)

    def getOrdersTpslPending(
        self,
        instId: Optional[str] = None,
        tpslId: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get pending TP/SL orders.
        
        Args:
            instId: Filter by instrument ID, e.g. BTC-USDT
            tpslId: TP/SL order ID
            clientOrderId: Client Order ID as assigned by the client.
                         A combination of case-sensitive alphanumerics, all numbers,
                         or all letters of up to 32 characters.
            before: Return records newer than the requested tpslId
            after: Return records older than the requested tpslId
            limit: Number of results per request. Max 100, default 20
            
        Returns:
            Dict: Response containing pending TP/SL orders:
                - tpslId: TP/SL order ID
                - clientOrderId: Client Order ID as assigned by the client
                - instId: Instrument ID
                - marginMode: Margin mode
                - positionSide: Position side
                - side: Order side
                - tpTriggerPrice: Take-profit trigger price
                - tpOrderPrice: Take-profit order price (-1 for market price)
                - slTriggerPrice: Stop-loss trigger price
                - slOrderPrice: Stop-loss order price (-1 for market price)
                - size: Number of contracts to buy or sell
                - state: State (live, effective, canceled, order_failed)
                - leverage: Leverage
                - reduceOnly: Whether orders can only reduce position size
                - actualSize: Actual order quantity
                - createTime: Creation time in milliseconds
                - brokerId: Broker ID provided by BloFin
                
        Note:
            The before and after parameters cannot be used simultaneously.
        """
        params = {}
        if instId:
            params["instId"] = instId
        if tpslId:
            params["tpslId"] = tpslId
        if clientOrderId:
            params["clientOrderId"] = clientOrderId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/orders-tpsl-pending', params=params)

    def getOrdersAlgoPending(
        self,
        instId: Optional[str] = None,
        algoId: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None,
        orderType: str = "trigger"
    ) -> Dict:
        """Get pending algo orders.
        
        Args:
            instId: Filter by instrument ID
            algoId: Filter by algo order ID
            clientOrderId: Filter by client order ID
            before: Return records newer than this order ID
            after: Return records older than this order ID
            limit: Number of results per request, max 100, default 20
            orderType: Algo type, currently only supports 'trigger'
            
        Returns:
            Dict: Response containing pending algo orders
        """
        params = {"orderType": orderType}
        if instId:
            params["instId"] = instId
        if algoId:
            params["algoId"] = algoId
        if clientOrderId:
            params["clientOrderId"] = clientOrderId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/orders-algo-pending', params=params)

    def getOrdersHistory(
        self,
        instId: Optional[str] = None,
        orderType: Optional[str] = None,
        state: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get completed order history.
        
        Args:
            instId: Instrument ID, e.g. BTC-USDT
            orderType: Order type
                - market: market order
                - limit: limit order
                - post_only: Post-only order
                - fok: Fill-or-kill order
                - ioc: Immediate-or-cancel order
            state: Order state
                - canceled: Canceled orders
                - filled: Filled orders
                - partially_canceled: Partially canceled orders (final state, has pnl if closing order)
            before: Return records newer than this order ID
            after: Return records older than this order ID (cannot be used with before)
            begin: Filter with begin timestamp (Unix timestamp in milliseconds, e.g. 1597026383085)
            end: Filter with end timestamp (Unix timestamp in milliseconds, e.g. 1597026383085)
            limit: Number of results per request, max 100, default 20
            
        Returns:
            Dict: Response containing detailed order history with fields:
                - orderId: Order ID
                - clientOrderId: Client-assigned Order ID
                - instId: Instrument ID
                - marginMode: Margin mode
                - positionSide: Position side (long/short/net)
                - side: Order side (buy/sell)
                - orderType: Order type
                - price: Order price
                - size: Order size
                - reduceOnly: Whether order only reduces position
                - leverage: Position leverage
                - state: Order state
                - filledSize: Accumulated fill quantity
                - pnl: Profit and loss (for closing orders)
                - averagePrice: Average filled price
                - fee: Fee and rebate
                - createTime: Creation timestamp (ms)
                - updateTime: Last update timestamp (ms)
                - orderCategory: Order category (normal/full_liquidation/partial_liquidation/adl/tp/sl)
                - tpTriggerPrice: Take-profit trigger price
                - tpOrderPrice: Take-profit order price (-1 for market)
                - slTriggerPrice: Stop-loss trigger price
                - slOrderPrice: Stop-loss order price (-1 for market)
                - cancelSource: Cancellation source type
                - cancelSourceReason: Reason for cancellation
                - algoClientOrderId: Algo order client ID
                - algoId: Algo order ID
                - brokerId: BloFin broker ID
        """
        params = {}
        if instId:
            params["instId"] = instId
        if orderType:
            params["orderType"] = orderType
        if state:
            params["state"] = state
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if begin:
            params["begin"] = begin
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/orders-history', params=params)

    def getOrdersTpslHistory(
        self,
        instId: Optional[str] = None,
        tpslId: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        state: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get TP/SL order history under the current account.
        
        Args:
            instId: Instrument ID, e.g. BTC-USDT
            tpslId: TP/SL order ID
            clientOrderId: Client Order ID (up to 32 alphanumeric characters)
            state: Order state (live/effective/canceled/order_failed)
            before: Return records newer than this tpslId
            after: Return records older than this tpslId (cannot be used with before)
            limit: Number of results per request, max 100, default 20
            
        Returns:
            Dict: Response containing TP/SL order history with fields:
                - tpslId: TP/SL order ID
                - clientOrderId: Client-assigned Order ID
                - instId: Instrument ID
                - marginMode: Margin mode
                - positionSide: Position side (long/short/net)
                - side: Order side
                - orderType: Order type (market/limit/post_only/fok/ioc)
                - size: Order size
                - reduceOnly: Whether order only reduces position (true/false)
                - leverage: Position leverage
                - state: Order state (live/effective/canceled/order_failed)
                - actualSize: Actual order quantity
                - orderCategory: Order category (normal/full_liquidation/partial_liquidation/adl/tp/sl)
                - tpTriggerPrice: Take-profit trigger price
                - tpOrderPrice: Take-profit order price (-1 for market)
                - slTriggerPrice: Stop-loss trigger price
                - slOrderPrice: Stop-loss order price (-1 for market)
                - createTime: Creation timestamp in milliseconds
                - brokerId: BloFin broker ID (up to 16 characters)
        """
        params = {}
        if instId:
            params["instId"] = instId
        if tpslId:
            params["tpslId"] = tpslId
        if clientOrderId:
            params["clientOrderId"] = clientOrderId
        if state:
            params["state"] = state
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/orders-tpsl-history', params=params)

    def getOrdersAlgoHistory(
        self,
        instId: Optional[str] = None,
        algoId: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        state: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None,
        orderType: str = "trigger"
    ) -> Dict:
        """Get algo orders history under the current account.
        
        Args:
            instId: Instrument ID, e.g. BTC-USDT
            algoId: Algo order ID
            clientOrderId: Client Order ID (up to 32 alphanumeric characters)
            state: Order state (live/effective/canceled/order_failed)
            before: Return records newer than this algoId
            after: Return records older than this algoId (cannot be used with before)
            limit: Number of results per request, max 100, default 20
            orderType: Algo type, currently only supports 'trigger'
            
        Returns:
            Dict: Response containing algo orders history with fields:
                - algoId: Algo order ID
                - clientOrderId: Client-assigned Order ID
                - instId: Instrument ID
                - marginMode: Margin mode
                - positionSide: Position side (long/short/net)
                - side: Order side
                - reduceOnly: Whether order only reduces position (true/false)
                - orderType: Algo type (trigger)
                - size: Order size
                - leverage: Position leverage
                - state: Order state (live/effective/canceled/order_failed)
                - actualSize: Actual order quantity
                - createTime: Creation timestamp in milliseconds
                - triggerPrice: Trigger price
                - triggerPriceType: Trigger price type (last: last price)
                - brokerId: BloFin broker ID (up to 16 characters)
                - attachAlgoOrders: Array of attached SL/TP orders with fields:
                    - tpTriggerPrice: Take-profit trigger price
                    - tpOrderPrice: Take-profit order price (-1 for market)
                    - tpTriggerPriceType: TP trigger price type (last)
                    - slTriggerPrice: Stop-loss trigger price
                    - slOrderPrice: Stop-loss order price (-1 for market)
                    - slTriggerPriceType: SL trigger price type (last)
        """
        params = {"orderType": orderType}
        if instId:
            params["instId"] = instId
        if algoId:
            params["algoId"] = algoId
        if clientOrderId:
            params["clientOrderId"] = clientOrderId
        if state:
            params["state"] = state
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/orders-algo-history', params=params)

    def getFillsHistory(
        self,
        instId: Optional[str] = None,
        orderId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get recently-filled transaction details.
        
        Args:
            instId: Instrument ID, e.g. BTC-USDT
            orderId: Order ID
            before: Return records newer than this tradeId
            after: Return records older than this tradeId (cannot be used with before)
            begin: Filter with begin timestamp (Unix timestamp in milliseconds, e.g. 1597026383085)
            end: Filter with end timestamp (Unix timestamp in milliseconds, e.g. 1597026383085)
            limit: Number of results per request, max 100, default 20
            
        Returns:
            Dict: Response containing fills history with fields:
                - instId: Instrument ID
                - tradeId: Trade ID
                - orderId: Order ID
                - fillPrice: Filled price
                - fillSize: Filled quantity
                - fillPnl: Last filled profit and loss (for closing positions)
                - positionSide: Position side (long/short/net)
                - side: Order side
                - fee: Fee
                - ts: Data generation time in milliseconds
                - brokerId: BloFin broker ID (up to 16 characters)
        """
        params = {}
        if instId:
            params["instId"] = instId
        if orderId:
            params["orderId"] = orderId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if begin:
            params["begin"] = begin
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/trade/fills-history', params=params)

    def getOrderPriceRange(self, instId: str, side: str) -> Dict:
        """Get order price range.
        
        Args:
            instId: Instrument ID
            side: Order side (buy/sell)
            
        Returns:
            Dict: Response containing price range information
        """
        params = {
            "instId": instId,
            "side": side
        }
        return self._client.get('/api/v1/trade/order/price-range', params=params)

    def queryApikey(self) -> Dict:
        """Query API key information.
        
        Returns:
            Dict: Response containing API key information
        """
        return self._client.get('/api/v1/user/query-apikey')

    def placeOrder(
        self,
        instId: str,
        marginMode: str,
        positionSide: str,
        side: str,
        orderType: str,
        size: str,
        price: Optional[str] = None,
        reduceOnly: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        tpTriggerPrice: Optional[str] = None,
        tpOrderPrice: Optional[str] = None,
        slTriggerPrice: Optional[str] = None,
        slOrderPrice: Optional[str] = None,
        brokerId: Optional[str] = None
    ) -> Dict:
        """Place an order.
        
        Args:
            instId: Required, Instrument ID, e.g. BTC-USDT
            marginMode: Required, Margin mode (cross/isolated)
            positionSide: Required, Position side:
                         - net: Default for One-way Mode
                         - long/short: Required for Hedge Mode
            side: Required, Order side (buy/sell)
            orderType: Required, Order type:
                      - market: Market order
                      - limit: Limit order
                      - post_only: Post-only order
                      - fok: Fill-or-kill order
                      - ioc: Immediate-or-cancel order
            size: Required, Number of contracts to buy/sell
            price: Optional, Order price (required for non-market orders)
            reduceOnly: Optional, Close position only (true/false, default false)
            clientOrderId: Optional, Client Order ID (max 32 chars)
            tpTriggerPrice: Optional, Take-profit trigger price
            tpOrderPrice: Optional, Take-profit order price (-1 for market)
            slTriggerPrice: Optional, Stop-loss trigger price
            slOrderPrice: Optional, Stop-loss order price (-1 for market)
            brokerId: Optional, Broker ID (max 16 chars)
            
        Returns:
            Dict: Response containing order result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List containing order info:
                    - orderId: Order ID
                    - clientOrderId: Client Order ID if specified
                    - code: Execution result code
                    - msg: Success/rejection message
                    
        Note:
            For position side:
            - Use 'net' for One-way Mode (default)
            - Must use 'long' or 'short' for Hedge Mode
            
            For TP/SL orders:
            - tpTriggerPrice and tpOrderPrice must be set together
            - slTriggerPrice and slOrderPrice must be set together
            - Use -1 as order price for market execution
            
            For reduceOnly:
            - When true, order size cannot exceed position size
            - Position will be fully closed with no new position
            
            For clientOrderId:
            - Max 32 characters
            - Can be alphanumeric, all numbers, or all letters
            
        Examples:
            >>> # Place a limit buy order
            >>> api.placeOrder(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="net",
            ...     side="buy",
            ...     orderType="limit",
            ...     price="23212.2",
            ...     size="2"
            ... )
            
            >>> # Place a market sell order with TP/SL
            >>> api.placeOrder(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="net",
            ...     side="sell",
            ...     orderType="market",
            ...     size="1",
            ...     tpTriggerPrice="24000",
            ...     tpOrderPrice="-1",
            ...     slTriggerPrice="22000",
            ...     slOrderPrice="-1"
            ... )
        """
        params = {
            "instId": instId,
            "marginMode": marginMode,
            "positionSide": positionSide,
            "side": side,
            "orderType": orderType,
            "size": size
        }
        
        if price is not None:
            params["price"] = price
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if clientOrderId is not None:
            params["clientOrderId"] = clientOrderId
        if tpTriggerPrice is not None:
            params["tpTriggerPrice"] = tpTriggerPrice
        if tpOrderPrice is not None:
            params["tpOrderPrice"] = tpOrderPrice
        if slTriggerPrice is not None:
            params["slTriggerPrice"] = slTriggerPrice
        if slOrderPrice is not None:
            params["slOrderPrice"] = slOrderPrice
        if brokerId is not None:
            params["brokerId"] = brokerId
            
        return self._client.post('/api/v1/trade/order', params)

    def placeBatchOrders(self, orders: List[Dict]) -> Dict:
        """Place multiple orders simultaneously.
        
        Args:
            orders: List of order dictionaries, each containing:
                Required parameters:
                - instId: Instrument ID, e.g. BTC-USDT
                - marginMode: Margin mode (cross/isolated)
                - positionSide: Position side (net/long/short)
                - side: Order side (buy/sell)
                - orderType: Order type (market/limit/post_only/fok/ioc)
                - size: Number of contracts to buy/sell
                - price: Order price (required except for market orders)
                
                Optional parameters:
                - reduceOnly: Close position only (true/false, default false)
                - clientOrderId: Client Order ID (max 32 chars)
                - tpTriggerPrice: Take-profit trigger price
                - tpOrderPrice: Take-profit order price (-1 for market)
                - slTriggerPrice: Stop-loss trigger price
                - slOrderPrice: Stop-loss order price (-1 for market)
                - brokerId: Broker ID (max 16 chars)
            
        Returns:
            Dict: Response containing batch order results:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of order results, each containing:
                    - orderId: Order ID
                    - clientOrderId: Client Order ID if specified
                    - code: Execution result code
                    - msg: Success/rejection message
                    
        Note:
            For position side:
            - Use 'net' for One-way Mode (default)
            - Must use 'long' or 'short' for Hedge Mode
            
            For TP/SL orders:
            - tpTriggerPrice and tpOrderPrice must be set together
            - slTriggerPrice and slOrderPrice must be set together
            - Use -1 as order price for market execution
            
            For reduceOnly:
            - When true, order size cannot exceed position size
            - Position will be fully closed with no new position
            
            For clientOrderId:
            - Max 32 characters
            - Can be alphanumeric, all numbers, or all letters
            
        Examples:
            >>> # Place two limit buy orders
            >>> api.placeBatchOrders([
            ...     {
            ...         "instId": "ETH-USDT",
            ...         "marginMode": "cross",
            ...         "positionSide": "net",
            ...         "side": "buy",
            ...         "orderType": "limit",
            ...         "price": "1601.1",
            ...         "size": "1",
            ...         "clientOrderId": "order1"
            ...     },
            ...     {
            ...         "instId": "ETH-USDT",
            ...         "marginMode": "cross",
            ...         "positionSide": "net",
            ...         "side": "buy",
            ...         "orderType": "limit",
            ...         "price": "1602.1",
            ...         "size": "2",
            ...         "clientOrderId": "order2"
            ...     }
            ... ])
            
            >>> # Place orders with TP/SL
            >>> api.placeBatchOrders([
            ...     {
            ...         "instId": "BTC-USDT",
            ...         "marginMode": "cross",
            ...         "positionSide": "net",
            ...         "side": "buy",
            ...         "orderType": "limit",
            ...         "price": "23000",
            ...         "size": "1",
            ...         "tpTriggerPrice": "24000",
            ...         "tpOrderPrice": "-1",
            ...         "slTriggerPrice": "22000",
            ...         "slOrderPrice": "-1"
            ...     }
            ... ])
        """
        return self._client.post('/api/v1/trade/batch-orders', orders)

    def placeTpsl(
        self,
        instId: str,
        marginMode: str,
        positionSide: str,
        side: str,
        size: str,
        tpTriggerPrice: str = None,
        tpOrderPrice: Optional[str] = None,
        slTriggerPrice: Optional[str] = None,
        slOrderPrice: Optional[str] = None,
        reduceOnly: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        brokerId: Optional[str] = None
    ) -> Dict:
        """Place a take-profit/stop-loss order.
        
        Args:
            instId: Required, Instrument ID, e.g. BTC-USDT
            marginMode: Required, Margin mode (cross/isolated)
            positionSide: Required, Position side:
                         - net: Default for One-way Mode
                         - long/short: Required for Hedge Mode
            side: Required, Order side (buy/sell)
            size: Required, Quantity (-1 for entire position)
            tpTriggerPrice: Take-profit trigger price
            tpOrderPrice: Optional, Take-profit order price (-1 for market)
            slTriggerPrice: Optional, Stop-loss trigger price
            slOrderPrice: Optional, Stop-loss order price (-1 for market)
            reduceOnly: Optional, Close position only (true/false, default false)
            clientOrderId: Optional, Client Order ID (max 32 chars)
            brokerId: Optional, Broker ID (max 16 chars)
            
        Returns:
            Dict: Response containing order result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Order information containing:
                    - tpslId: TP/SL order ID
                    - clientOrderId: Client Order ID if specified
                    - code: Execution result code
                    - msg: Success/rejection message
                    
        Note:
            For position side:
            - Use 'net' for One-way Mode (default)
            - Must use 'long' or 'short' for Hedge Mode
            
            For TP/SL prices:
            - tpTriggerPrice and tpOrderPrice must be set together
            - slTriggerPrice and slOrderPrice must be set together
            - Use -1 as order price for market execution
            
            For size:
            - Use -1 to close entire position
            
            For reduceOnly:
            - When true, order size cannot exceed position size
            - Position will be fully closed with no new position
            
        Examples:
            >>> # Place a TP order at market price
            >>> api.placeTpsl(
            ...     instId="ETH-USDT",
            ...     marginMode="cross",
            ...     positionSide="net",
            ...     side="sell",
            ...     size="1",
            ...     tpTriggerPrice="1661.1",
            ...     tpOrderPrice="-1"
            ... )
            
            >>> # Place both TP and SL orders
            >>> api.placeTpsl(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="short",
            ...     side="buy",
            ...     size="-1",  # Close entire position
            ...     tpTriggerPrice="24000",
            ...     tpOrderPrice="-1",
            ...     slTriggerPrice="26000",
            ...     slOrderPrice="-1",
            ...     reduceOnly="true"
            ... )
        """
        params = {
            "instId": instId,
            "marginMode": marginMode,
            "positionSide": positionSide,
            "side": side,
            "size": size
        }
        
        if tpTriggerPrice is not None:
            params["tpTriggerPrice"] = tpTriggerPrice
        if tpOrderPrice is not None:
            params["tpOrderPrice"] = tpOrderPrice
        if slTriggerPrice is not None:
            params["slTriggerPrice"] = slTriggerPrice
        if slOrderPrice is not None:
            params["slOrderPrice"] = slOrderPrice
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if clientOrderId is not None:
            params["clientOrderId"] = clientOrderId
        if brokerId is not None:
            params["brokerId"] = brokerId
            
        return self._client.post('/api/v1/trade/order-tpsl', params)

    def placeAlgoOrder(
        self,
        instId: str,
        marginMode: str,
        positionSide: str,
        side: str,
        size: str,
        orderType: str,
        triggerPrice: str,
        orderPrice: Optional[str] = None,
        triggerPriceType: Optional[str] = None,
        reduceOnly: Optional[str] = None,
        clientOrderId: Optional[str] = None,
        brokerId: Optional[str] = None,
        attachAlgoOrders: Optional[List[Dict]] = None
    ) -> Dict:
        """Place an algorithmic order (currently supports trigger orders).
        
        Args:
            instId: Required, Instrument ID, e.g. BTC-USDT
            marginMode: Required, Margin mode (cross/isolated)
            positionSide: Required, Position side:
                         - net: Default for One-way Mode
                         - long/short: Required for Hedge Mode
            side: Required, Order side (buy/sell)
            size: Required, Quantity (-1 for entire position)
            orderType: Required, Currently only supports "trigger"
            triggerPrice: Required, Price at which the order is triggered
            orderPrice: Optional, Order price (-1 for market price)
            triggerPriceType: Optional, Price type for trigger (last)
            reduceOnly: Optional, Close position only (true/false, default false)
            clientOrderId: Optional, Client Order ID (max 32 chars)
            brokerId: Optional, Broker ID (max 16 chars)
            attachAlgoOrders: Optional, List of attached TP/SL orders, each containing:
                - tpTriggerPrice: Take-profit trigger price
                - tpOrderPrice: Take-profit order price (-1 for market)
                - tpTriggerPriceType: TP trigger price type (last)
                - slTriggerPrice: Stop-loss trigger price
                - slOrderPrice: Stop-loss order price (-1 for market)
                - slTriggerPriceType: SL trigger price type (last)
            
        Returns:
            Dict: Response containing order result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Order information containing:
                    - algoId: Algo order ID
                    - clientOrderId: Client Order ID if specified
                    - code: Execution result code
                    - msg: Success/rejection message
                    
        Note:
            For position side:
            - Use 'net' for One-way Mode (default)
            - Must use 'long' or 'short' for Hedge Mode
            
            For trigger orders:
            - Currently only supports "trigger" as orderType
            - Use -1 as orderPrice for market execution
            
            For size:
            - Use -1 to close entire position
            
            For reduceOnly:
            - When true, order size cannot exceed position size
            - Position will be fully closed with no new position
            
            For attached TP/SL:
            - Must provide both trigger price and order price
            - Use -1 as order price for market execution
            
        Examples:
            >>> # Place a trigger order
            >>> api.placeAlgoOrder(
            ...     instId="ETH-USDT",
            ...     marginMode="cross",
            ...     positionSide="short",
            ...     side="sell",
            ...     size="1",
            ...     orderType="trigger",
            ...     triggerPrice="3000",
            ...     orderPrice="-1",  # Market price
            ...     triggerPriceType="last"
            ... )
            
            >>> # Place trigger order with TP/SL
            >>> api.placeAlgoOrder(
            ...     instId="ETH-USDT",
            ...     marginMode="cross",
            ...     positionSide="short",
            ...     side="sell",
            ...     size="1",
            ...     orderType="trigger",
            ...     triggerPrice="3000",
            ...     orderPrice="-1",
            ...     attachAlgoOrders=[{
            ...         "tpTriggerPrice": "3500",
            ...         "tpOrderPrice": "3600",
            ...         "tpTriggerPriceType": "last",
            ...         "slTriggerPrice": "2600",
            ...         "slOrderPrice": "2500",
            ...         "slTriggerPriceType": "last"
            ...     }]
            ... )
        """
        params = {
            "instId": instId,
            "marginMode": marginMode,
            "positionSide": positionSide,
            "side": side,
            "size": size,
            "orderType": orderType,
            "triggerPrice": triggerPrice
        }
        
        if orderPrice is not None:
            params["orderPrice"] = orderPrice
        if triggerPriceType is not None:
            params["triggerPriceType"] = triggerPriceType
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if clientOrderId is not None:
            params["clientOrderId"] = clientOrderId
        if brokerId is not None:
            params["brokerId"] = brokerId
        if attachAlgoOrders is not None:
            params["attachAlgoOrders"] = attachAlgoOrders
            
        return self._client.post('/api/v1/trade/order-algo', params)

    def cancelOrder(self, orderId: str, instId: Optional[str] = None, clientOrderId: Optional[str] = None) -> Dict:
        """Cancel an existing order.
        
        Args:
            orderId: Order ID
            instId: Instrument ID (optional)
            clientOrderId: Client Order ID (optional). A combination of case-sensitive 
                         alphanumerics, all numbers, or all letters of up to 32 characters.
            
        Returns:
            Dict: Response containing cancellation result:
                - orderId: Order ID
                - clientOrderId: Client Order ID as assigned by the client
                - code: The code of the event execution result, 0 means success
                - msg: Rejection or success message of event execution
        """
        data = {"orderId": orderId}
        if instId:
            data["instId"] = instId
        if clientOrderId:
            data["clientOrderId"] = clientOrderId
            
        return self._client.post('/api/v1/trade/cancel-order', data)

    def cancelBatchOrders(self, orders: List[Dict]) -> Dict:
        """Cancel multiple orders in a single request.
        
        Args:
            orders: List of order parameters, each containing:
                   - orderId: Required, Order ID
                   - instId: Optional, Instrument ID, e.g. BTC-USDT
                   - clientOrderId: Optional, Client Order ID as assigned by the client.
                     A combination of case-sensitive alphanumerics, all numbers,
                     or all letters of up to 32 characters.
            
        Returns:
            Dict: Response containing cancellation results:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of cancellation results, each containing:
                    - orderId: Order ID
                    - clientOrderId: Client Order ID as assigned by the client
                    - code: The code of the event execution result, 0 means success
                    - msg: Rejection or success message if cancellation failed
                    
        Examples:
            >>> # Cancel multiple orders
            >>> api.cancelBatchOrders([
            ...     {"orderId": "22619976", "instId": "ETH-USDT"},
            ...     {"orderId": "22619977", "instId": "ETH-USDT"}
            ... ])
        """
        data = []
        for order in orders:
            if "orderId" not in order:
                raise ValueError("orderId is required for each order in batch cancellation")
                
            order_data = {"orderId": order["orderId"]}
            if "instId" in order:
                order_data["instId"] = order["instId"]
            if "clientOrderId" in order:
                order_data["clientOrderId"] = order["clientOrderId"]
            data.append(order_data)
            
        return self._client.post('/api/v1/trade/cancel-batch-orders', data)

    def cancelTpsl(
        self,
        orders: List[Dict],
    ) -> Dict:
        """Cancel one or more TP/SL orders.
        
        Args:
            orders: List of order parameters, each containing:
                - tpslId: Optional, TP/SL order ID
                - clientOrderId: Optional, Client Order ID as assigned by the client.
                  A combination of case-sensitive alphanumerics, all numbers,
                  or all letters of up to 32 characters.
            
        Returns:
            Dict: Response containing cancellation results:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of cancellation results, each containing:
                    - tpslId: TP/SL order ID
                    - clientOrderId: Client Order ID as assigned by the client
                    - code: The code of the event execution result, 0 means success
                    - msg: Rejection or success message of event execution
                    
        Examples:
            >>> # Cancel a single TP/SL order
            >>> api.cancelTpsl([{
            ...     "tpslId": "22619976"
            ... }])
            
            >>> # Cancel multiple TP/SL orders
            >>> api.cancelTpsl([
            ...     {"tpslId": "22619976"},
            ...     {"tpslId": "22619977"}
            ... ])
        """
        return self._client.post('/api/v1/trade/cancel-tpsl', orders)

    def cancelAlgoOrder(self, instId: Optional[str] = None, algoId: Optional[str] = None, clientOrderId: Optional[str] = None) -> Dict:
        """Cancel an algo order.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            algoId: Optional, Algo order ID
            clientOrderId: Optional, Client Order ID as assigned by the client.
                         A combination of case-sensitive alphanumerics, all numbers,
                         or all letters of up to 32 characters.
            
        Returns:
            Dict: Response containing cancellation result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Cancellation result containing:
                    - algoId: Algo order ID
                    - clientOrderId: Client Order ID
                    - code: The code of the event execution result
                    - msg: Rejection or success message
        """
        data = {}
        if instId:
            data["instId"] = instId
        if algoId:
            data["algoId"] = algoId
        if clientOrderId:
            data["clientOrderId"] = clientOrderId
            
        return self._client.post('/api/v1/trade/cancel-algo', data)

    def closePosition(
        self,
        instId: str,
        marginMode: str,
        positionSide: str,
        clientOrderId: Optional[str] = None,
        brokerId: Optional[str] = None
    ) -> Dict:
        """Close a position via a market order.
        
        Args:
            instId: Required, Instrument ID, e.g. BTC-USDT
            marginMode: Required, Margin mode ('cross' or 'isolated')
            positionSide: Required, Position side.
                         Default 'net' for One-way Mode.
                         Must be 'long' or 'short' for Hedge Mode.
            clientOrderId: Optional, Client Order ID as assigned by the client.
                         A combination of case-sensitive alphanumerics, all numbers,
                         or all letters of up to 32 characters.
            brokerId: Optional, Broker ID provided by BloFin.
                     A combination of case-sensitive alphanumerics, all numbers,
                     or all letters of up to 16 characters.
            
        Returns:
            Dict: Response containing operation result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Operation result containing:
                    - instId: Instrument ID
                    - positionSide: Position side (long/short/net)
                    - clientOrderId: Client Order ID
                    
        Examples:
            >>> # Close a position in One-way Mode
            >>> api.closePosition(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="net"
            ... )
            
            >>> # Close a long position in Hedge Mode
            >>> api.closePosition(
            ...     instId="BTC-USDT",
            ...     marginMode="isolated",
            ...     positionSide="long",
            ...     clientOrderId="my_close_1"
            ... )
        """
        data = {
            "instId": instId,
            "marginMode": marginMode,
            "positionSide": positionSide
        }
        if clientOrderId:
            data["clientOrderId"] = clientOrderId
        if brokerId:
            data["brokerId"] = brokerId
            
        return self._client.post('/api/v1/trade/close-position', data)

    def setMarginMode(self, marginMode: str) -> Dict:
        """Set margin mode.
        
        Args:
            marginMode: Margin mode to set
            
        Returns:
            Dict: Response containing operation result
        """
        data = {"marginMode": marginMode}
        return self._client.post('/api/v1/account/set-margin-mode', data)

    def setPositionMode(self, positionMode: str) -> Dict:
        """Set position mode.
        
        Args:
            positionMode: Position mode to set. "long_short_mode" or "net_mode"
            
        Returns:
            Dict: Response containing operation result
        """
        data = {"positionMode": positionMode}
        return self._client.post('/api/v1/account/set-position-mode', data)

    def setLeverage(
        self,
        instId: str,
        leverage: str,
        marginMode: str,
        positionSide: Optional[str] = None
    ) -> Dict:
        """Set leverage.
        
        Args:
            instId: Instrument ID, e.g. BTC-USDT
            leverage: Leverage to set
            marginMode: Margin mode, either 'cross' or 'isolated'
            positionSide: Optional, Position side ('long' or 'short').
                         Only required when margin mode is isolated in long/short mode.
            
        Returns:
            Dict: Response containing operation result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Operation result containing:
                    - instId: Instrument ID
                    - leverage: Leverage
                    - marginMode: Margin mode
                    - positionSide: Position side (long/short/net)
                    
        Examples:
            >>> # Set cross margin leverage
            >>> api.setLeverage(
            ...     instId="BTC-USDT",
            ...     leverage="100",
            ...     marginMode="cross"
            ... )
            
            >>> # Set isolated margin leverage for long position
            >>> api.setLeverage(
            ...     instId="BTC-USDT",
            ...     leverage="100",
            ...     marginMode="isolated",
            ...     positionSide="long"
            ... )
        """
        data = {
            "instId": instId,
            "leverage": leverage,
            "marginMode": marginMode
        }
        if positionSide:
            data["positionSide"] = positionSide
            
        return self._client.post('/api/v1/account/set-leverage', data)
