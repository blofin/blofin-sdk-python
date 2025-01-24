from typing import Dict, Optional
from .client import Client

class CopyTradingAPI:
    """BloFin Copy Trading REST API client.
    
    Handles all copy trading related endpoints including account management,
    positions, orders and trading operations.
    """
    
    def __init__(self, client: Client):
        self._client = client

    # Account endpoints
    def getInstruments(self) -> Dict:
        """Get available instruments for copy trading.
        
        Returns:
            Dict: Response containing available instruments
        """
        return self._client.get('/api/v1/copytrading/instruments')

    def getConfig(self) -> Dict:
        """Get copy trading configuration.
        
        Returns:
            Dict: Response containing copy trading configuration
        """
        return self._client.get('/api/v1/copytrading/config')

    def getAccountBalance(self) -> Dict:
        """Get copy trading account balance.
        
        Returns:
            Dict: Response containing account balance information
        """
        return self._client.get('/api/v1/copytrading/account/balance')

    def getPositionsDetailsByOrder(self, orderId: str) -> Dict:
        """Get position close history details by order.
        
        Args:
            orderId: Required, Order ID
            
        Returns:
            Dict: Response containing position close details:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Close history containing:
                    - orderList: List of close orders, each containing:
                        - closeOrderId: Close order ID
                        - instId: Instrument ID, e.g. BTC-USDT
                        - positionSide: Position side (long/short/net)
                        - closeType: Close type (close/liquidation/adl/tp/sl)
                        - side: Order side (buy/sell)
                        - orderTime: Order create time in milliseconds
                        - size: Order amount
                        - filledAmount: Filled amount
                        - averagePrice: Average open price
                        - fee: Fee
                        - realizedPnl: Realized PnL of this order
                        - realizedPnlRatio: Realized PnL ratio of this order
                        - brokerId: Optional, Broker ID provided by BloFin
                        
        Note:
            For positionSide:
            - In long/short mode: positions are always positive
            - In net mode: positive positions means long position,
              negative positions means short position
            
        Examples:
            >>> # Get close history for an order
            >>> api.getPositionsDetailsByOrder(orderId="1216365")
        """
        params = {"orderId": orderId}
        return self._client.get('/api/v1/copytrading/account/positions-details-by-order', params=params)

    def getPositionMode(self) -> Dict:
        """Get position mode setting.
        
        Returns:
            Dict: Response containing position mode information
        """
        return self._client.get('/api/v1/copytrading/account/position-mode')

    def getLeverageInfo(self, instId: str, marginMode: str) -> Dict:
        """Get leverage information.
        
        Args:
            instId: Required, Instrument ID(s). Can be a single instrument ID
                   or multiple IDs separated by commas (max 20), e.g. "BTC-USDT"
                   or "BTC-USDT,ETH-USDT"
            marginMode: Required, Margin mode ('cross' or 'isolated')
            
        Returns:
            Dict: Response containing leverage information:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of leverage information, each containing:
                    - instId: Instrument ID
                    - leverage: Leverage
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side (long/short/net)
                    
        Raises:
            ValueError: If more than 20 instrument IDs are provided
            
        Examples:
            >>> # Get leverage info for a single instrument
            >>> api.getLeverageInfo(
            ...     instId="BTC-USDT",
            ...     marginMode="cross"
            ... )
            
            >>> # Get leverage info for multiple instruments
            >>> api.getLeverageInfo(
            ...     instId="BTC-USDT,ETH-USDT",
            ...     marginMode="isolated"
            ... )
        """
        if instId.count(',') >= 20:
            raise ValueError("Cannot query more than 20 instrument IDs at once")
            
        params = {
            "instId": instId,
            "marginMode": marginMode
        }
        return self._client.get('/api/v1/copytrading/account/leverage-info', params=params)

    def getPositionsByContract(self, instId: Optional[str] = None) -> Dict:
        """Get positions in "By Contract" mode.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            
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
                    - adl: ADL lever
                    - leverage: Leverage
                    - positions: Quantity of positions
                    - availablePositions: Position that can be closed
                    - averagePrice: Average open price
                    - markPrice: Mark Price
                    - marginRatio: Margin Ratio
                    - liquidationPrice: Estimated liquidation price
                    - unrealizedPnl: Unrealized profit and loss
                    - unrealizedPnlRatio: Unrealized profit and loss ratio
                    - initialMargin: Initial margin requirement (cross only)
                    - maintenanceMargin: Maintenance margin requirement
                    - createTime: Creation time in milliseconds
                    - updateTime: Last adjustment time in milliseconds
                    
        Note:
            For positionSide:
            - In long/short mode: positions are always positive
            - In net mode: positive positions means long position,
              negative positions means short position
            
        Examples:
            >>> # Get all positions
            >>> api.getPositionsByContract()
            
            >>> # Get positions for specific instrument
            >>> api.getPositionsByContract(instId="BTC-USDT")
        """
        params = {}
        if instId:
            params["instId"] = instId
            
        return self._client.get('/api/v1/copytrading/account/positions-by-contract', params=params)

    def getPositionsByOrder(
        self,
        instId: Optional[str] = None,
        orderId: Optional[str] = None,
        limit: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> Dict:
        """Get positions information in order mode.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            orderId: Optional, Order ID
            limit: Optional, Number of results per request (max 20, default 20)
            after: Optional, Return records earlier than this orderId
            before: Optional, Return records newer than this orderId
            
        Returns:
            Dict: Response containing positions information:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of positions, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - instType: Instrument type
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side (long/short/net)
                    - leverage: Leverage
                    - positions: Quantity of positions (unchanged by closing trades)
                    - availablePositions: Position that can be closed
                    - averagePrice: Average open price
                    - markPrice: Latest Mark price
                    - unrealizedPnl: Unrealized profit and loss
                    - unrealizedPnlRatio: Unrealized profit and loss ratio
                    - realizedPnl: Realized profit and loss
                    - createTime: Order create time in milliseconds
                    - updateTime: Update time in milliseconds
                    
        Note:
            For positionSide:
            - In long/short mode: positions are always positive
            - In net mode: positive positions means long position,
              negative positions means short position
            
        Examples:
            >>> # Get all positions
            >>> api.getPositionsByOrder()
            
            >>> # Get positions for specific instrument
            >>> api.getPositionsByOrder(instId="BTC-USDT")
            
            >>> # Get positions with pagination
            >>> api.getPositionsByOrder(
            ...     limit="10",
            ...     after="254098"
            ... )
        """
        params = {}
        if instId:
            params["instId"] = instId
        if orderId:
            params["orderId"] = orderId
        if limit:
            params["limit"] = limit
        if after:
            params["after"] = after
        if before:
            params["before"] = before
            
        return self._client.get('/api/v1/copytrading/account/positions-by-order', params=params)

    def getOrdersPending(
        self,
        instId: Optional[str] = None,
        orderType: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get active (incomplete) orders under the current account.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            orderType: Optional, Order type:
                      - market: market order
                      - limit: limit order
                      - post_only: Post-only order
                      - fok: Fill-or-kill order
                      - ioc: Immediate-or-cancel order
            state: Optional, Order state:
                   - live
                   - partially_filled
            after: Optional, Return records earlier than this orderId
            before: Optional, Return records newer than this orderId
            limit: Optional, Number of results per request (max 100, default 20)
            
        Note:
            The before and after parameters cannot be used simultaneously.
            
        Returns:
            Dict: Response containing pending orders:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of orders, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode
                    - positionSide: Position side
                    - side: Order side
                    - orderType: Order type
                    - price: Price
                    - size: Number of contracts
                    - reduceOnly: Whether order only reduces position size
                    - leverage: Leverage
                    - state: Order state
                    - filledSize: Accumulated fill quantity
                    - averagePrice: Average filled price
                    - pnl: Profit and loss
                    - createTime: Creation time in milliseconds
                    - updateTime: Update time in milliseconds
                    - tpTriggerPrice: Take-profit trigger price
                    - tpOrderPrice: Take-profit order price (-1 for market)
                    - slTriggerPrice: Stop-loss trigger price
                    - slOrderPrice: Stop-loss order price (-1 for market)
                    - brokerId: Optional, Broker ID
                    
        Examples:
            >>> # Get all pending orders
            >>> api.getOrdersPending()
            
            >>> # Get pending orders for specific instrument
            >>> api.getOrdersPending(instId="BTC-USDT")
            
            >>> # Get pending market orders
            >>> api.getOrdersPending(orderType="market")
            
            >>> # Get partially filled orders with pagination
            >>> api.getOrdersPending(
            ...     state="partially_filled",
    ...     limit="50"
    ... )
        """
        if after is not None and before is not None:
            raise ValueError("The before and after parameters cannot be used simultaneously")
            
        params = {}
        if instId:
            params["instId"] = instId
        if orderType:
            params["orderType"] = orderType
        if state:
            params["state"] = state
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/copytrading/trade/orders-pending', params=params)

    def getPendingTpslByContract(
        self,
        instId: Optional[str] = None,
        algoId: Optional[str] = None
    ) -> Dict:
        """Get active TP/SL orders in "By Contract" mode.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            algoId: Optional, Algo order ID
            
        Returns:
            Dict: Response containing active TP/SL orders:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of TP/SL orders, each containing:
                    - algoId: TP/SL order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side
                    - tpTriggerPrice: Take-profit trigger price
                    - tpOrderPrice: Take-profit order price (-1 for market)
                    - slTriggerPrice: Stop-loss trigger price
                    - slOrderPrice: Stop-loss order price (-1 for market)
                    - size: Quantity (-1 for entire position)
                    - state: State (live/effective/canceled/order_failed)
                    - leverage: Leverage
                    - actualSize: Actual order quantity
                    - createTime: Creation time in milliseconds
                    - brokerId: Optional, Broker ID
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For order prices:
            - If tpOrderPrice or slOrderPrice is -1, the order will be
              executed at market price
            
            For size:
            - If size is -1, it means the entire position will be closed
            
        Examples:
            >>> # Get all active TP/SL orders
            >>> api.getPendingTpslByContract()
            
            >>> # Get TP/SL orders for specific instrument
            >>> api.getPendingTpslByContract(instId="BTC-USDT")
        
        """
        params = {}
        if instId:
            params["instId"] = instId
        if algoId:
            params["algoId"] = algoId
            
        return self._client.get('/api/v1/copytrading/trade/pending-tpsl-by-contract', params=params)

    def getPositionHistoryByOrder(
        self,
        instId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get position history in "By Order" mode.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            before: Optional, Return records earlier than this orderId
            after: Optional, Return records newer than this orderId
            limit: Optional, Number of results per request (max 20, default 20)
            
        Returns:
            Dict: Response containing position history:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of positions, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - leverage: Leverage
                    - positionSide: Position side
                    - orderSide: Order side (buy/sell)
                    - positions: Positions amount
                    - createTime: Order create time in milliseconds
                    - openAveragePrice: Average open price
                    - closeTime: Closing time in milliseconds
                    - closeAveragePrice: Average closing price
                    - pnl: PnL
                    - pnlRatio: PnL ratio
                    - copiers: Number of successful copiers
                    - closeType: Close type (manual/liquidation/adl/tp/sl/multiple)
                    - preSharing: Pre-sharing Amount
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For closeType:
            - manual: Manually closed
            - liquidation: Liquidation
            - adl: Auto-deleveraging
            - tp: Take profit
            - sl: Stop loss
            - multiple: Multiple close types
            
        Examples:
            >>> # Get all position history
            >>> api.getPositionHistoryByOrder()
            
            >>> # Get history for specific instrument
            >>> api.getPositionHistoryByOrder(instId="BTC-USDT")
            
            >>> # Get history with pagination
            >>> api.getPositionHistoryByOrder(
            ...     instId="BTC-USDT",
            ...     limit="10"
            ... )
        """
        params = {}
        if instId:
            params["instId"] = instId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/copytrading/trade/position-history-by-order', params=params)

    def getOrdersHistory(
        self,
        instId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get order history.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            before: Optional, Return records earlier than this orderId
            after: Optional, Return records newer than this orderId
            limit: Optional, Number of results per request (max 20, default 20)
            
        Returns:
            Dict: Response containing order history:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of orders, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side
                    - side: Order side (buy/sell)
                    - orderType: Order type
                    - price: Order price
                    - size: Number of contracts
                    - leverage: Leverage
                    - state: Order state
                    - filledSize: Accumulated fill quantity
                    - pnl: PnL
                    - averagePrice: Average filled price
                    - fee: Fee and rebate
                    - createTime: Order create time in milliseconds
                    - updateTime: Update time in milliseconds
                    - orderCategory: Order category
                    - brokerId: Optional, Broker ID
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For orderCategory:
            - normal: Normal order
            - liquidation: Liquidation order
            - adl: Auto-deleveraging order
            - tp: Take profit order
            - sl: Stop loss order
            
            For size:
            - Refer to /api/v1/market/instruments for contract size details
            
        Examples:
            >>> # Get all order history
            >>> api.getOrdersHistory()
            
            >>> # Get history for specific instrument
            >>> api.getOrdersHistory(instId="BTC-USDT")
            
            >>> # Get history with pagination
            >>> api.getOrdersHistory(
            ...     instId="BTC-USDT",
            ...     limit="10"
            ... )
        """
        params = {}
        if instId:
            params["instId"] = instId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/copytrading/trade/orders-history', params=params)

    def getOrdersPending(
        self,
        instId: Optional[str] = None,
        orderType: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get active (incomplete) orders under the current account.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            orderType: Optional, Order type:
                      - market: market order
                      - limit: limit order
                      - post_only: Post-only order
                      - fok: Fill-or-kill order
                      - ioc: Immediate-or-cancel order
            state: Optional, Order state:
                   - live
                   - partially_filled
            after: Optional, Return records earlier than this orderId
            before: Optional, Return records newer than this orderId
            limit: Optional, Number of results per request (max 100, default 20)
            
        Note:
            The before and after parameters cannot be used simultaneously.
            
        Returns:
            Dict: Response containing pending orders:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of orders, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode
                    - positionSide: Position side
                    - side: Order side
                    - orderType: Order type
                    - price: Price
                    - size: Number of contracts
                    - reduceOnly: Whether order only reduces position size
                    - leverage: Leverage
                    - state: Order state
                    - filledSize: Accumulated fill quantity
                    - averagePrice: Average filled price
                    - pnl: Profit and loss
                    - createTime: Creation time in milliseconds
                    - updateTime: Update time in milliseconds
                    - tpTriggerPrice: Take-profit trigger price
                    - tpOrderPrice: Take-profit order price (-1 for market)
                    - slTriggerPrice: Stop-loss trigger price
                    - slOrderPrice: Stop-loss order price (-1 for market)
                    - brokerId: Optional, Broker ID
                    
        Examples:
            >>> # Get all pending orders
            >>> api.getOrdersPending()
            
            >>> # Get pending orders for specific instrument
            >>> api.getOrdersPending(instId="BTC-USDT")
            
            >>> # Get pending market orders
            >>> api.getOrdersPending(orderType="market")
            
            >>> # Get partially filled orders with pagination
            >>> api.getOrdersPending(
            ...     state="partially_filled",
    ...     limit="50"
    ... )
        """
        if after is not None and before is not None:
            raise ValueError("The before and after parameters cannot be used simultaneously")
            
        params = {}
        if instId:
            params["instId"] = instId
        if orderType:
            params["orderType"] = orderType
        if state:
            params["state"] = state
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/copytrading/trade/orders-pending', params=params)

    def getPendingTpslByContract(
        self,
        instId: Optional[str] = None,
        algoId: Optional[str] = None
    ) -> Dict:
        """Get active TP/SL orders in "By Contract" mode.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            algoId: Optional, Algo order ID
            
        Returns:
            Dict: Response containing active TP/SL orders:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of TP/SL orders, each containing:
                    - algoId: TP/SL order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side
                    - tpTriggerPrice: Take-profit trigger price
                    - tpOrderPrice: Take-profit order price (-1 for market)
                    - slTriggerPrice: Stop-loss trigger price
                    - slOrderPrice: Stop-loss order price (-1 for market)
                    - size: Quantity (-1 for entire position)
                    - state: State (live/effective/canceled/order_failed)
                    - leverage: Leverage
                    - actualSize: Actual order quantity
                    - createTime: Creation time in milliseconds
                    - brokerId: Optional, Broker ID
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For order prices:
            - If tpOrderPrice or slOrderPrice is -1, the order will be
              executed at market price
            
            For size:
            - If size is -1, it means the entire position will be closed
            
        Examples:
            >>> # Get all active TP/SL orders
            >>> api.getPendingTpslByContract()
            
            >>> # Get TP/SL orders for specific instrument
            >>> api.getPendingTpslByContract(instId="BTC-USDT")
        
        """
        params = {}
        if instId:
            params["instId"] = instId
        if algoId:
            params["algoId"] = algoId
            
        return self._client.get('/api/v1/copytrading/trade/pending-tpsl-by-contract', params=params)

    def getPositionHistoryByOrder(
        self,
        instId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get position history in "By Order" mode.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            before: Optional, Return records earlier than this orderId
            after: Optional, Return records newer than this orderId
            limit: Optional, Number of results per request (max 20, default 20)
            
        Returns:
            Dict: Response containing position history:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of positions, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - leverage: Leverage
                    - positionSide: Position side
                    - orderSide: Order side (buy/sell)
                    - positions: Positions amount
                    - createTime: Order create time in milliseconds
                    - openAveragePrice: Average open price
                    - closeTime: Closing time in milliseconds
                    - closeAveragePrice: Average closing price
                    - pnl: PnL
                    - pnlRatio: PnL ratio
                    - copiers: Number of successful copiers
                    - closeType: Close type (manual/liquidation/adl/tp/sl/multiple)
                    - preSharing: Pre-sharing Amount
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For closeType:
            - manual: Manually closed
            - liquidation: Liquidation
            - adl: Auto-deleveraging
            - tp: Take profit
            - sl: Stop loss
            - multiple: Multiple close types
            
        Examples:
            >>> # Get all position history
            >>> api.getPositionHistoryByOrder()
            
            >>> # Get history for specific instrument
            >>> api.getPositionHistoryByOrder(instId="BTC-USDT")
            
            >>> # Get history with pagination
            >>> api.getPositionHistoryByOrder(
            ...     instId="BTC-USDT",
            ...     limit="10"
            ... )
        """
        params = {}
        if instId:
            params["instId"] = instId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/copytrading/trade/position-history-by-order', params=params)

    def getOrdersHistory(
        self,
        instId: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get order history.
        
        Args:
            instId: Optional, Instrument ID, e.g. BTC-USDT
            before: Optional, Return records earlier than this orderId
            after: Optional, Return records newer than this orderId
            limit: Optional, Number of results per request (max 20, default 20)
            
        Returns:
            Dict: Response containing order history:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of orders, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side
                    - side: Order side (buy/sell)
                    - orderType: Order type
                    - price: Order price
                    - size: Number of contracts
                    - leverage: Leverage
                    - state: Order state
                    - filledSize: Accumulated fill quantity
                    - pnl: PnL
                    - averagePrice: Average filled price
                    - fee: Fee and rebate
                    - createTime: Order create time in milliseconds
                    - updateTime: Update time in milliseconds
                    - orderCategory: Order category
                    - brokerId: Optional, Broker ID
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For orderCategory:
            - normal: Normal order
            - liquidation: Liquidation order
            - adl: Auto-deleveraging order
            - tp: Take profit order
            - sl: Stop loss order
            
            For size:
            - Refer to /api/v1/market/instruments for contract size details
            
        Examples:
            >>> # Get all order history
            >>> api.getOrdersHistory()
            
            >>> # Get history for specific instrument
            >>> api.getOrdersHistory(instId="BTC-USDT")
            
            >>> # Get history with pagination
            >>> api.getOrdersHistory(
            ...     instId="BTC-USDT",
            ...     limit="10"
            ... )
        """
        params = {}
        if instId:
            params["instId"] = instId
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/copytrading/trade/orders-history', params=params)

    def getPendingTpslByOrder(
        self,
        orderId: str
    ) -> Dict:
        """Get active TP/SL orders in "By Order" mode.
        
        Args:
            orderId: Required, Order ID
            
        Returns:
            Dict: Response containing active TP/SL orders:
                - code: Response code, "0" means success
                - msg: Response message
                - data: List of TP/SL orders, each containing:
                    - orderId: Order ID
                    - instId: Instrument ID
                    - marginMode: Margin mode (cross/isolated)
                    - positionSide: Position side
                    - tpTriggerPrice: Take-profit trigger price
                    - tpOrderPrice: Take-profit order price (-1 for market)
                    - slTriggerPrice: Stop-loss trigger price
                    - slOrderPrice: Stop-loss order price (-1 for market)
                    - size: Quantity (-1 for entire position)
                    - state: State (live/effective/canceled/order_failed)
                    - leverage: Leverage
                    - createTime: Creation time in milliseconds
                    - brokerId: Optional, Broker ID
                    
        Note:
            For positionSide:
            - Default 'net' for One-way Mode
            - Must be 'long' or 'short' for Hedge Mode
            
            For order prices:
            - If tpOrderPrice or slOrderPrice is -1, the order will be
              executed at market price
            
            For size:
            - If size is -1, it means the entire position will be closed
            
            For state:
            - live: Order is live
            - effective: Order is effective
            - canceled: Order was canceled
            - order_failed: Order failed
            
        Examples:
            >>> # Get TP/SL orders for a specific order
            >>> api.getPendingTpslByOrder(orderId="144265765")
        """
        params = {"orderId": orderId}
        return self._client.get('/api/v1/copytrading/trade/pending-tpsl-by-order', params=params)

    def cancelTpslByContract(self, algoId: str) -> Dict:
        """Cancel take profit/stop loss order by contract.
        
        Args:
            algoId: TP/SL order ID to cancel
            
        Returns:
            Dict: Response containing:
                code (str): Result code, "0" means success
                msg (str): Result message
                
        Example Response:
            {
                "code": "0",
                "msg": "success"
            }
        """
        data = {"algoId": algoId}
        return self._client.post('/api/v1/copytrading/trade/cancel-tpsl-by-contract', data)

    def cancelTpslByOrder(self, orderId: str) -> Dict:
        """Cancel take profit/stop loss order by order.
        
        Args:
            orderId: Order ID to cancel TP/SL
            
        Returns:
            Dict: Response containing:
                code (str): Result code, "0" means success
                msg (str): Result message
                
        Example Response:
            {
                "code": "0",
                "msg": "success"
            }
        """
        data = {
            "orderId": orderId
        }
        return self._client.post('/api/v1/copytrading/trade/cancel-tpsl-by-order', data)

    # POST methods
    def setPositionMode(self, positionMode: str) -> Dict:
        """Set position mode.
        
        Args:
            positionMode: Position mode to set. "long_short_mode" or "net_mode"
            
        Returns:
            Dict: Response containing operation result
        """
        data = {"positionMode": positionMode}
        return self._client.post('/api/v1/copytrading/account/set-position-mode', data)

    def setLeverage(self, instId: str, leverage: str, marginMode: str, positionSide: str) -> Dict:
        """Set leverage.
        
        Args:
            instId: Instrument ID
            leverage: Leverage to set
            marginMode: Margin mode to set. "cross" or "isolated"
            
        Returns:
            Dict: Response containing operation result
        """
        data = {
            "instId": instId,
            "leverage": leverage,
            "marginMode": marginMode,
            "positionSide": positionSide
        }
        return self._client.post('/api/v1/copytrading/account/set-leverage', data)

    def placeOrder(
        self,
        instId: str,
        marginMode: str,
        positionSide: str,
        side: str,
        orderType: str,
        size: str,
        price: Optional[str] = None,
        brokerId: Optional[str] = None
    ) -> Dict:
        """Place an order in copy trading.
        
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
                      - fok: Fill-or-kill order
                      - ioc: Immediate-or-cancel order
            size: Required, Number of contracts to buy/sell
            price: Optional, Order price (required for non-market orders)
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
            
            For brokerId:
            - Max 16 characters
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
            
            >>> # Place a market sell order
            >>> api.placeOrder(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="long",
            ...     side="sell",
            ...     orderType="market",
            ...     size="1"
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
        if brokerId is not None:
            params["brokerId"] = brokerId
            
        return self._client.post('/api/v1/copytrading/trade/place-order', params)

    def cancelOrder(self, orderId: str) -> Dict:
        """Cancel a copy trading order.
        
        Args:
            orderId: Order ID to cancel
            
        Returns:
            Dict: Response containing:
                code (str): Result code, "0" means success
                msg (str): Result message
                data (Dict): Contains detailed result:
                    code (str): Inner result code
                    msg (str): Inner result message
                
        Example Response:
            {
                "code": "0",
                "msg": "success",
                "data": {
                    "code": "0",
                    "msg": null
                }
            }
        """
        data = {
            "orderId": orderId
        }
        return self._client.post('/api/v1/copytrading/trade/cancel-order', data)

    def placeTpslByContract(
        self,
        instId: str,
        marginMode: str,
        positionSide: str,
        tpTriggerPrice: str,
        slTriggerPrice: str,
        size: str,
        type: Optional[str] = None,
        brokerId: Optional[str] = None
    ) -> Dict:
        """Place take profit/stop loss order by contract.
        
        Args:
            instId: Required, Instrument ID, e.g. BTC-USDT
            marginMode: Required, Margin mode (cross/isolated)
            positionSide: Required, Position side:
                         - net: Default for One-way Mode
                         - long/short: Required for Hedge Mode
            tpTriggerPrice: Required, Take-profit trigger price
            slTriggerPrice: Required, Stop-loss trigger price
            size: Required, Quantity. Use "-1" for entire position
            type: Optional, TP/SL Type:
                  - pnl: Close by the order of pnl volume (default)
                  - fixedRatio: Close all orders with same ratio (e.g. 0.1 = 10%)
            brokerId: Optional, Broker ID (max 16 chars)
            
        Returns:
            Dict: Response containing order result:
                - code: Response code, "0" means success
                - msg: Response message
                - data: Order info containing:
                    - algoId: TP/SL order ID
                    
        Examples:
            >>> # Place TP/SL for entire short position
            >>> api.placeTpslByContract(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="short",
            ...     tpTriggerPrice="80000",
            ...     slTriggerPrice="101000",
            ...     size="-1"
            ... )
            
            >>> # Place TP/SL for partial long position with fixed ratio
            >>> api.placeTpslByContract(
            ...     instId="BTC-USDT",
            ...     marginMode="cross",
            ...     positionSide="long",
            ...     tpTriggerPrice="85000",
            ...     slTriggerPrice="75000",
            ...     size="0.1",
            ...     type="fixedRatio"
            ... )
        """
        params = {
            "instId": instId,
            "marginMode": marginMode,
            "positionSide": positionSide,
            "tpTriggerPrice": tpTriggerPrice,
            "slTriggerPrice": slTriggerPrice,
            "size": size
        }
        
        if type is not None:
            params["type"] = type
        if brokerId is not None:
            params["brokerId"] = brokerId
            
        return self._client.post('/api/v1/copytrading/trade/place-tpsl-by-contract', params)

    def placeTpslByOrder(
        self,
        orderId: str,
        tpTriggerPrice: str,
        slTriggerPrice: str,
        size: str,
        brokerId: Optional[str] = None
    ) -> Dict:
        """Place take profit/stop loss order by order ID.
        
        Args:
            orderId: Required, Order ID to place TP/SL for
            tpTriggerPrice: Required, Take-profit trigger price
            slTriggerPrice: Required, Stop-loss trigger price
            size: Required, Quantity. Use "-1" for entire position
            brokerId: Optional, Broker ID (max 16 chars)
            
        Returns:
            Dict: Response containing order result:
                - code: Response code, "0" means success
                - msg: Response message
                    
        Examples:
            >>> # Place TP/SL for entire position
            >>> api.placeTpslByOrder(
            ...     orderId="23209016",
            ...     tpTriggerPrice="80000",
            ...     slTriggerPrice="70000",
            ...     size="-1"
            ... )
            
            >>> # Place TP/SL for partial position
            >>> api.placeTpslByOrder(
            ...     orderId="23209016",
            ...     tpTriggerPrice="85000",
            ...     slTriggerPrice="75000",
            ...     size="0.1",
            ...     brokerId="test123"
            ... )
        """
        params = {
            "orderId": orderId,
            "tpTriggerPrice": tpTriggerPrice,
            "slTriggerPrice": slTriggerPrice,
            "size": size
        }
        
        if brokerId is not None:
            params["brokerId"] = brokerId
            
        return self._client.post('/api/v1/copytrading/trade/place-tpsl-by-order', params)

    def closePositionByOrder(self, orderId: str, size: str, brokerId: Optional[str] = None) -> Dict:
        """Close position by order.
        
        Args:
            orderId: Order ID to close
            size: Size to close
            brokerId: Optional broker ID provided by BloFin.
                     A combination of case-sensitive alphanumerics, all numbers,
                     or all letters of up to 16 characters.
            
        Returns:
            Dict: Response containing:
                code (str): Result code, "0" means success
                msg (str): Result message
                
        Example Response:
            {
                "code": "0",
                "msg": "success"
            }
        """
        data = {
            "orderId": orderId,
            "size": size
        }
        if brokerId:
            data["brokerId"] = brokerId
        return self._client.post('/api/v1/copytrading/trade/close-position-by-order', data)

    def closePositionByContract(self, instId: str, size: str, marginMode: str, positionSide: str, closeType: str,  brokerId: Optional[str] = None) -> Dict:
        """Close position by contract.
        
        Args:
            instId: Instrument ID
            size: Size to close
            marginMode: Margin mode (cross/isolated)
            positionSide: Position side (long/short)
            closeType: Close type (pnl/fixedRatio)
            brokerId: Broker ID (optional) 
        Returns:
            Dict: Response containing operation result
        """
        data = {
            "instId": instId,
            "size": size,
            "marginMode": marginMode,
            "positionSide": positionSide,
            "closeType": closeType
        }
        if brokerId:
            data["brokerId"] = brokerId
        return self._client.post('/api/v1/copytrading/trade/close-position-by-contract', data)
