"""BloFin WebSocket API client implementation."""

import asyncio
import json
import logging
import hmac
import hashlib
import time
import base64
from typing import AsyncIterator, Dict, Optional, Tuple
import websockets
from blofin.exceptions import BlofinAPIException
from blofin.logger_config import get_logger

logger = get_logger("websocket")

"""BloFin WebSocket API client with simplified reconnection mechanism."""

import asyncio
import json
import logging
import time
import websockets
from typing import Dict, Optional, Set, Any, AsyncIterator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("blofin_ws")

class BlofinWsClient:
    """BloFin WebSocket client with simplified connection management."""
    
    # WebSocket endpoints
    PUBLIC_WS_URL = "wss://openapi.blofin.com/ws/public"
    PRIVATE_WS_URL = "wss://openapi.blofin.com/ws/private" 
    
    def __init__(self, apiKey: str = "", secret: str = "", passphrase: str = "",
                 isPublic: bool = False, isCopytrading: bool = False):
        """Initialize WebSocket client.
        
        Args:
            apiKey: API access key for private endpoints
            secret: API secret for private endpoints
            passphrase: API passphrase for private endpoints
            isPublic: If True, use public endpoint without authentication
            isCopytrading: If True, use copytrading endpoint
        """
        # Auth credentials
        self.apiKey = apiKey
        self.secret = secret  
        self.passphrase = passphrase
        self.isPublic = isPublic
        self.isCopytrading = isCopytrading
        
        # Connection config
        if isCopytrading:
            self.url = "wss://openapi.blofin.com/ws/copytrading/private"
        else:
            self.url = self.PUBLIC_WS_URL if isPublic else self.PRIVATE_WS_URL
        
        # Connection state
        self._ws = None
        self._connected = False
        
        # Message handling
        self._messageQueue = asyncio.Queue()
        self._subscriptions: Set[str] = set()
        
        # Tasks
        self._heartbeatTask = None
        self._receiverTask = None
        
        # Reconnection state management  
        self._reconnectState = {
            'attempting': False,
            'maxRetries': 3,
            'retryDelay': 0.5, 
            'currentRetry': 0
        }

    def _isConnected(self) -> bool:
        """Check if WebSocket is connected."""
        return (
            self._ws is not None and 
            self._ws.state.value == 1  # OPEN state
        )

    async def connect(self) -> bool:
        """Establish WebSocket connection with authentication if needed.
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Create WebSocket connection
            self._ws = await websockets.connect(
                self.url,
                ping_interval=5,
                ping_timeout=3
            )
            
            # Authenticate for private endpoint
            if not self.isPublic:
                if not await self._authenticate():
                    await self._ws.close()
                    return False
                    
            # Start background tasks
            self._startTasks()
            
            self._connected = True
            logger.info("WebSocket connected successfully")
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise BlofinAPIException(
                message=f"WebSocket connection failed: {str(e)}"
            )

    async def _authenticate(self) -> bool:
        """Authenticate WebSocket connection for private endpoints.
        
        Returns:
            bool: True if authentication successful
        """
        try:
            # Generate auth signature
            timestamp = str(int(time.time() * 1000))
            signature, nonce = self._generateSignature(timestamp)
            
            # Send auth message
            authMessage = {
                "op": "login",
                "args": [{
                    "apiKey": self.apiKey,
                    "passphrase": self.passphrase,
                    "timestamp": timestamp,
                    "sign": signature,
                    "nonce": nonce
                }]
            }
            
            await self._ws.send(json.dumps(authMessage))
            
            # Wait for auth response
            response = await asyncio.wait_for(self._ws.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            if response_data.get("event") == "login" and response_data.get("code", "0") == "0":
                logger.info("Authentication successful")
                return True
            else:
                error_msg = response_data.get("msg", "Authentication failed")
                logger.error(f"Authentication failed: {error_msg}")
                raise BlofinAPIException(
                    message=f"WebSocket authentication failed: {error_msg}",
                    code=response_data.get("code"),
                    data=response_data.get("data")
                )
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise BlofinAPIException(
                message=f"WebSocket authentication error: {str(e)}"
            )

    def _generateSignature(self, timestamp: str) -> Tuple[str, str]:
        """Generate authentication signature.
        
        Args:
            timestamp: Current timestamp string
            
        Returns:
            Tuple[str, str]: (signature, nonce)
        """
        # Use timestamp as nonce
        nonce = timestamp
        
        # Fixed components for WebSocket auth
        method = "GET"
        path = "/users/self/verify"
        body = ""
        
        # Create signature string
        msg = f"{path}{method}{timestamp}{nonce}{body}"
        
        # Generate HMAC-SHA256 signature
        hexSignature = hmac.new(
            self.secret.encode(),
            msg.encode(),
            hashlib.sha256
        ).hexdigest().encode()
        
        # Convert to base64
        return base64.b64encode(hexSignature).decode(), nonce

    async def _reconnect(self) -> bool:
        """Handle WebSocket reconnection with exponential backoff.
        
        Returns:
            bool: True if reconnection successful
        """
        if self._reconnectState['attempting']:
            return False
            
        try:
            self._reconnectState['attempting'] = True
            
            while self._reconnectState['currentRetry'] < self._reconnectState['maxRetries']:
                try:
                    logger.info(f"Reconnection attempt {self._reconnectState['currentRetry'] + 1}")
                    
                    # Close existing connection
                    if self._ws:
                        await self._ws.close()
                        self._ws = None
                        
                    # Create new connection
                    self._ws = await websockets.connect(
                        self.url,
                        ping_interval=5,
                        ping_timeout=3
                    )
                    
                    # Re-authenticate if needed
                    if not self.isPublic:
                        if not await self._authenticate():
                            raise Exception("Re-authentication failed")
                            
                    # Restore subscriptions
                    subscriptions_to_restore = self._subscriptions.copy()
                    for subscription in subscriptions_to_restore:
                        # For private channels, don't include instId if it's "all"
                        if ":" in subscription:
                            channel, instId = subscription.split(":")
                            if instId == "all" and not self.isPublic:
                                await self.subscribe(channel)
                            else:
                                await self.subscribe(channel, instId)
                        else:
                            await self.subscribe(subscription)
                        
                    # Reset reconnection state
                    self._reconnectState['currentRetry'] = 0
                    self._connected = True
                    
                    # Restart background tasks
                    self._startTasks()
                    
                    logger.info("Reconnection successful")
                    return True
                    
                except Exception as e:
                    self._reconnectState['currentRetry'] += 1
                    if self._reconnectState['currentRetry'] < self._reconnectState['maxRetries']:
                        delay = self._reconnectState['retryDelay'] * (2 ** self._reconnectState['currentRetry'])
                        logger.info(f"Reconnection failed, retrying in {delay}s")
                        await asyncio.sleep(delay)
                    else:
                        logger.error("Maximum reconnection attempts reached")
                        raise BlofinAPIException(
                            message=f"WebSocket reconnection failed after {self._reconnectState['maxRetries']} attempts"
                        )
                        
            return False
            
        finally:
            self._reconnectState['attempting'] = False
            self._reconnectState['currentRetry'] = 0

    def _startTasks(self):
        """Start background tasks for message handling and heartbeat."""
        if not self._receiverTask or self._receiverTask.done():
            self._receiverTask = asyncio.create_task(self._messageReceiver())
            
        if not self._heartbeatTask or self._heartbeatTask.done():
            self._heartbeatTask = asyncio.create_task(self._heartbeatLoop())

    async def _messageReceiver(self):
        """Background task to receive and process WebSocket messages."""
        try:
            while True:
                try:
                    if not self._isConnected():
                        if not await self._handleDisconnect():
                            break
                        continue
                        
                    # Receive message with timeout
                    message = await asyncio.wait_for(self._ws.recv(), timeout=10)
                    
                    if message == "pong":
                        continue
                        
                    # Process message
                    data = json.loads(message)
                    await self._handleMessage(data)
                    
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Error receiving message: {e}")
                    if not self._connected and not await self._handleDisconnect():
                        break
                        
        except asyncio.CancelledError:
            logger.info("Message receiver cancelled")

    async def _handleDisconnect(self) -> bool:
        """Handle connection loss with reconnection attempt.
        
        Returns:
            bool: True if connection restored
        """
        self._connected = False
        if self._subscriptions:
            return await self._reconnect()
        return False

    async def _handleMessage(self, data: Dict):
        """Process received WebSocket message.
        
        Args:
            data: Parsed message data
        """
        try:
            # Handle different message types
            msgType = data.get("event") or data.get("op")
            
            if msgType == "error":
                logger.error(f"Error message received: {data}")
                return
                
            if msgType == "subscribe":
                await self._handleSubscriptionResponse(data)
                return
                
            # Queue message for client
            await self._messageQueue.put(data)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            raise BlofinAPIException(
                message=f"Error handling WebSocket message: {str(e)}"
            )

    async def _handleSubscriptionResponse(self, data: Dict):
        """Handle subscription confirmation messages.
        
        Args:
            data: Subscription response data
        """
        if "arg" not in data:
            logger.error(f"Invalid subscription response format: {data}")
            return
            
        channel = data["arg"].get("channel")
        instId = data["arg"].get("instId", "all")
        subscription = f"{channel}:{instId}"
        
        # Check for subscription errors
        if data.get("event") == "error" or data.get("code", "0") != "0":
            error_msg = data.get("msg", "Unknown error")
            error_code = data.get("code", "")
            logger.error(f"Subscription failed: {subscription}. Error {error_code}: {error_msg}")
            
            # Remove from subscriptions if it was added
            if subscription in self._subscriptions:
                self._subscriptions.remove(subscription)
                
            return
            
        # Successful subscription
        self._subscriptions.add(subscription)
        logger.info(f"Subscription confirmed: {subscription}")

    async def subscribe(self, channel: str, instId: Optional[str] = None) -> bool:
        """Subscribe to a WebSocket channel.
        
        Args:
            channel: Channel name to subscribe
            instId: Optional instrument ID
            
        Returns:
            bool: True if subscription request sent successfully
            
        Note:
            The actual subscription status will be handled by the message receiver task.
            Subscribe failures will be logged as errors.
        """
        try:
            # Prepare subscription message
            subMessage = {
                "op": "subscribe",
                "args": [{
                    "channel": channel
                }]
            }
            
            # Add instId only if it's provided and not None
            if instId is not None:
                subMessage["args"][0]["instId"] = instId
                
            # Send subscription request
            if not self._isConnected():
                if not await self._reconnect():
                    return False
                    
            await self._ws.send(json.dumps(subMessage))
            logger.info(f"Subscription requested: {channel}:{instId or 'all'}")
            
            return True
            
        except Exception as e:
            logger.error(f"Subscription error: {e}")
            raise BlofinAPIException(
                message=f"Subscription error: {str(e)}"
            )

    async def unsubscribe(self, channel: str, instId: Optional[str] = None) -> bool:
        """Unsubscribe from a WebSocket channel.
        
        Args:
            channel: Channel name to unsubscribe from
            instId: Optional instrument ID
            
        Returns:
            bool: True if unsubscription successful
        """
        try:
            # Prepare unsubscribe message
            unsubMessage = {
                "op": "unsubscribe",
                "args": [{
                    "channel": channel
                }]
            }
            
            # Add instId only if it's provided
            if instId:
                unsubMessage["args"][0]["instId"] = instId
                
            # Send unsubscription request
            if self._isConnected():
                await self._ws.send(json.dumps(unsubMessage))
                
            # Remove subscription
            if instId is not None:
                self._subscriptions.discard(f"{channel}:{instId}")
            else:
                self._subscriptions.discard(channel)
            logger.info(f"Unsubscribed from: {channel}:{instId or 'all'}")
            
            return True
            
        except Exception as e:
            logger.error(f"Unsubscription error: {e}")
            raise BlofinAPIException(
                message=f"Unsubscription error: {str(e)}"
            )

    async def _heartbeatLoop(self):
        """Maintain connection with periodic heartbeats."""
        try:
            while True:
                try:
                    if not self._isConnected():
                        break
                        
                    # Send ping
                    await self._ws.send("ping")
                    logger.debug("Ping sent")
                    
                    # Wait for next heartbeat
                    await asyncio.sleep(15)
                    
                except Exception as e:
                    logger.error(f"Heartbeat error: {e}")
                    if not await self._handleDisconnect():
                        break
                    
        except asyncio.CancelledError:
            logger.info("Heartbeat loop cancelled")

    async def listen(self) -> AsyncIterator[Dict]:
        """Listen for incoming WebSocket messages.
        
        Yields:
            Dict: Received message data
        """
        while True:
            try:
                # Get message from queue
                message = await self._messageQueue.get()
                yield message
                self._messageQueue.task_done()
                
            except Exception as e:
                logger.error(f"Error in message listener: {e}")
                if not self._connected and not await self._handleDisconnect():
                    break

    async def close(self):
        """Close WebSocket connection and cleanup."""
        try:
            # Cancel background tasks
            if self._receiverTask:
                self._receiverTask.cancel()
                
            if self._heartbeatTask:
                self._heartbeatTask.cancel()
                
            # Close WebSocket connection
            if self._ws:
                await self._ws.close()
                
            self._connected = False
            logger.info("WebSocket connection closed")
            
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
            raise BlofinAPIException(
                message=f"Error closing WebSocket connection: {str(e)}"
            )


class BlofinWsPublicClient(BlofinWsClient):
    """BloFin public WebSocket API client.
    Example:
        ```python
        async with BlofinWsPublicClient() as client:
            await client.connect()
            await client.subscribeTrades(instId="BTC-USDT")
            await client.subscribeOrderBook(instId="BTC-USDT")
            async for message in client.listen():
                print(message)  # Process each message
        ``` 
    """

    def __init__(self):
        """Initialize public WebSocket client."""
        super().__init__(isPublic=True)

    async def subscribeTrades(self, instId: str) -> bool:
        """Subscribe to trades channel. Data will be pushed whenever there is a trade.
        Every update contains only one trade.
        
        Args:
            instId: Instrument ID (e.g. "BTC-USDT")
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            instId: Instrument ID
            tradeId: Trade ID
            price: Trade price
            size: Trade size
            side: Trade direction ('buy' or 'sell')
            ts: Filled time in milliseconds
            
        Example of push data:
            {
                "arg": {
                    "channel": "trades",
                    "instId": "ETH-USDT"
                },
                "data": [{
                    "instId": "ETH-USDT",
                    "tradeId": "106074994",
                    "price": "1640.4",
                    "size": "1",
                    "side": "sell",
                    "ts": "1696646190511"
                }]
            }
        """
        return await self.subscribe("trades", instId)
        
    async def subscribeOrderBook(self, instId: str, depth: str = "books") -> bool:
        """Subscribe to order book channel.
        
        Args:
            instId: Instrument ID (e.g. "BTC-USDT")
            depth: Depth level option:
                  - "books": 200 depth levels, initial full snapshot followed by 
                           incremental updates every 100ms
                  - "books5": 5 depth levels, full snapshot every 100ms when changed
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            action: Push data type
                   - "snapshot": Full snapshot
                   - "update": Incremental update
            data: Subscribed data containing:
                - asks: Order book on sell side, array of [price, size]
                - bids: Order book on buy side, array of [price, size]
                - ts: Order book generation time in milliseconds
                - prevSeqId: Previous sequence ID (0 for snapshot)
                - seqId: Current sequence ID
                
        Example of push data (snapshot):
            {
                "arg": {
                    "channel": "books",
                    "instId": "ETH-USDT"
                },
                "action": "snapshot",
                "data": {
                    "asks": [
                        [1639.75, 392],   # [price, size]
                        [1639.95, 541]
                    ],
                    "bids": [
                        [1639.7, 6817],
                        [1639.65, 4744]
                    ],
                    "ts": "1696670727520",
                    "prevSeqId": "0",
                    "seqId": "107600747"
                }
            }
            
        Notes:
            1. For books (200 levels):
               - Initial push is a full snapshot
               - Subsequent pushes are incremental updates
               - Use prevSeqId and seqId to maintain order
               - Update local orderbook:
                 * If price exists: Update size (remove if size=0)
                 * If new price: Insert and sort (bids descending, asks ascending)
            
            2. For books5 (5 levels):
               - Every push is a full snapshot
               - No need to handle incremental updates
        """
        if depth not in ["books", "books5"]:
            raise ValueError("depth must be either 'books' or 'books5'")
        return await self.subscribe(depth, instId)
        
    async def subscribeTickers(self, instId: str) -> bool:
        """Subscribe to tickers channel. Data will be pushed at most every 1 second.
        
        Args:
            instId: Instrument ID (e.g. "BTC-USDT")
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            instId: Instrument ID
            last: Last traded price
            lastSize: Last traded size
            askPrice: Best ask price
            askSize: Best ask size
            bidPrice: Best bid price
            bidSize: Best bid size
            open24h: Open price in the past 24 hours
            high24h: Highest price in the past 24 hours
            low24h: Lowest price in the past 24 hours
            volCurrency24h: 24h trading volume in base currency
            vol24h: 24h trading volume in contracts
            ts: Ticker data generation time in milliseconds
            
        Example of push data:
            {
                "arg": {
                    "channel": "tickers",
                    "instId": "BTC-USDT"
                },
                "data": [{
                    "instId": "BTC-USDT",
                    "last": "9999.99",
                    "lastSize": "0.1",
                    "askPrice": "9999.99",
                    "askSize": "11",
                    "bidPrice": "8888.88",
                    "bidSize": "5",
                    "open24h": "9000",
                    "high24h": "10000",
                    "low24h": "8888.88",
                    "volCurrency24h": "2222",
                    "vol24h": "2222",
                    "ts": "1597026383085"
                }]
            }
        """
        return await self.subscribe("tickers", instId)
        
    async def subscribeCandles(self, instId: str, interval: str = "1m") -> bool:
        """Subscribe to candlestick channel.
        
        Args:
            instId: Instrument ID (e.g. "BTC-USDT")
            interval: Candlestick interval. Available values:
                     - "1m": 1 minute
                     - "3m": 3 minutes
                     - "5m": 5 minutes
                     - "15m": 15 minutes
                     - "30m": 30 minutes
                     - "1H": 1 hour
                     - "2H": 2 hours
                     - "4H": 4 hours
                     - "6H": 6 hours
                     - "8H": 8 hours
                     - "12H": 12 hours
                     - "1D": 1 day
                     - "3D": 3 days
                     - "1W": 1 week
                     - "1M": 1 month
                     Default is "1m"
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            ts: Opening time of the candlestick in milliseconds
            open: Open price
            high: Highest price
            low: Lowest price
            close: Close price
            vol: Trading volume (contracts)
            volCurrency: Trading volume (base currency)
            volCurrencyQuote: Trading volume (quote currency)
            confirm: Candlestick state (0: uncompleted, 1: completed)
        """
        channel = f"candle{interval}"
        return await self.subscribe(channel, instId)
        
    async def subscribeFundingRate(self, instId: str) -> bool:
        """Subscribe to funding rate channel. Data will be pushed at most every 30 seconds.
        
        Args:
            instId: Instrument ID (e.g. "BTC-USDT")
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            instId: Instrument ID
            fundingRate: Current funding rate
            fundingTime: Funding time of the upcoming settlement in milliseconds
            
        Example of push data:
            {
                "arg": {
                    "channel": "funding-rate",
                    "instId": "BTC-USDT"
                },
                "data": [{
                    "fundingRate": "0.0001875391284828",
                    "fundingTime": "1700726400000",
                    "instId": "BTC-USDT"
                }]
            }
        """
        return await self.subscribe("funding-rate", instId)

class BlofinWsPrivateClient(BlofinWsClient):
    """Client for private WebSocket endpoints.
    
    Provides access to authenticated user data channels:
    - Orders
    - Positions 
    - Account updates
    - Algo orders
    """
    
    def __init__(self, apiKey: str, secret: str, passphrase: str):
        """Initialize private WebSocket client.
        
        Args:
            apiKey: API access key
            secret: API secret key
            passphrase: API passphrase
        """
        super().__init__(apiKey=apiKey, secret=secret, passphrase=passphrase)
        
    async def subscribeOrders(self, instId: Optional[str] = None) -> bool:
        """Subscribe to orders channel. Data will only be pushed when there are order updates.
        
        Args:
            instId: Optional instrument ID. If None, subscribes to all instruments.
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            action: Push data type ("snapshot" for full, "update" for incremental)
            data: Array of order information containing:
                instId: Instrument ID (e.g. "BTC-USDT")
                instType: Instrument type
                orderId: Order ID
                clientOrderId: Client-assigned order ID
                price: Order price
                size: Order size (number of contracts)
                orderType: Order type
                side: Order side
                positionSide: Position side
                marginMode: Margin mode
                filledSize: Accumulated fill quantity
                filledAmount: Filled amount
                averagePrice: Average filled price
                state: Order state
                leverage: Position leverage
                tpTriggerPrice: Take-profit trigger price
                tpOrderPrice: Take-profit order price (-1 for market price)
                slTriggerPrice: Stop-loss trigger price
                slOrderPrice: Stop-loss order price (-1 for market price)
                fee: Fee and rebate
                pnl: Profit and loss
                cancelSource: Cancel source
                orderCategory: Order category (normal/full_liquidation/partial_liquidation/adl/tp/sl)
                createTime: Creation time in milliseconds
                updateTime: Update time in milliseconds
                reduceOnly: Whether order can only reduce position size
                brokerId: Broker ID (up to 16 characters)
            
        Example of push data:
            {
                "action": "snapshot",
                "arg": {
                    "channel": "orders"
                },
                "data": [{
                    "instType": "SWAP",
                    "instId": "BTC-USDT",
                    "orderId": "28334314",
                    "clientOrderId": null,
                    "price": "28000.000000000000000000",
                    "size": "10",
                    "orderType": "limit",
                    "side": "sell",
                    "positionSide": "net",
                    "marginMode": "cross",
                    "filledSize": "0",
                    "filledAmount": "0.000000000000000000",
                    "averagePrice": "0.000000000000000000",
                    "state": "live",
                    "leverage": "2",
                    "tpTriggerPrice": "27000.000000000000000000",
                    "tpOrderPrice": "-1",
                    "slTriggerPrice": null,
                    "slOrderPrice": null,
                    "fee": "0.000000000000000000",
                    "pnl": "0.000000000000000000",
                    "cancelSource": "",
                    "orderCategory": "pre_tp_sl",
                    "createTime": "1696760245931",
                    "updateTime": "1696760245973",
                    "reduceOnly": "false",
                    "brokerId": ""
                }]
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
            Data will not be pushed when first subscribed, only on order updates.
        """
        return await self.subscribe("orders", instId)
        
    async def subscribePositions(self, instId: Optional[str] = None) -> bool:
        """Subscribe to positions channel. Initial snapshot will be pushed on subscription.
        Data will be pushed on events (order placement/cancellation) and at regular intervals.
        
        Args:
            instId: Optional instrument ID. If None, subscribes to all instruments.
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            data: Array of position information containing:
                instId: Instrument ID (e.g. "BTC-USDT")
                instType: Instrument type
                marginMode: Margin mode ("cross" or "isolated")
                positionId: Position ID
                positionSide: Position side ("long", "short", or "net")
                    Note: For "net", positive means long, negative means short
                positions: Quantity of positions
                availablePositions: Position that can be closed
                averagePrice: Average open price
                unrealizedPnl: Unrealized profit and loss (mark price)
                unrealizedPnlRatio: Unrealized profit and loss ratio
                leverage: Position leverage
                liquidationPrice: Estimated liquidation price
                markPrice: Latest mark price
                initialMargin: Initial margin requirement (cross mode only)
                margin: Margin (can be added or reduced)
                marginRatio: Margin ratio
                maintenanceMargin: Maintenance margin requirement
                adl: Auto decrease line level (1-5, lower means weaker)
                createTime: Creation time in milliseconds
                updateTime: Latest adjustment time in milliseconds
            
        Example of push data:
            {
                "arg": {
                    "channel": "positions"
                },
                "data": [{
                    "instType": "SWAP",
                    "instId": "BNB-USDT",
                    "marginMode": "cross",
                    "positionId": "8138",
                    "positionSide": "net",
                    "positions": "-100",
                    "availablePositions": "-100",
                    "averagePrice": "130.06",
                    "unrealizedPnl": "-77.1",
                    "unrealizedPnlRatio": "-1.778409964631708442",
                    "leverage": "3",
                    "liquidationPrice": "107929.699398660166170462",
                    "markPrice": "207.16",
                    "initialMargin": "69.053333333333333333",
                    "margin": "",
                    "marginRatio": "131.337873621866389829",
                    "maintenanceMargin": "1.0358",
                    "adl": "3",
                    "createTime": "1695795726481",
                    "updateTime": "1695795726484"
                }]
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
        """
        return await self.subscribe("positions", instId)
        
    async def subscribeAccount(self) -> bool:
        """Subscribe to account channel for real-time account updates.

        This channel uses private WebSocket and requires authentication. Data will be pushed when 
        triggered by events such as order placement, cancellation, execution, etc. It will also 
        be pushed at regular intervals.

        Returns:
            bool: True if subscription successful, False otherwise

        Request Format:
            {
                "op": "subscribe",
                "args": [{
                    "channel": "account"
                }]
            }

        Success Response:
            {
                "event": "subscribe",
                "arg": {
                    "channel": "account"
                }
            }

        Error Response:
            {
                "event": "error",
                "code": "60012",
                "msg": "Invalid request: {...}"
            }

        Push Data Parameters:
            arg (Object): Successfully subscribed channel info
                channel (str): Channel name
            data (Object): Account information containing:
                ts (str): Update time in milliseconds
                totalEquity (str): Total equity in USD
                isolatedEquity (str): Isolated margin equity in USD
                details (List[Object]): Array of currency details, each containing:
                    currency (str): Currency name
                    equity (str): Currency equity
                    balance (str): Cash balance
                    ts (str): Currency balance update time in milliseconds
                    isolatedEquity (str): Isolated margin equity in this currency
                    available (str): Available balance
                    availableEquity (str): Available equity
                    frozen (str): Frozen balance
                    orderFrozen (str): Margin frozen for open orders
                    equityUsd (str): Equity in USD
                    isolatedUnrealizedPnl (str): Isolated unrealized profit/loss
                    coinUsdPrice (str): Price index USD of currency
                    spotAvailable (str): Spot balance of the currency
                    liability (str): Liabilities of currency (Multi-currency margin)
                    borrowFrozen (str): Potential borrowing IMR in USD (Multi-currency margin)
                    marginRatio (str): Cross maintenance margin requirement (Multi-currency margin)

        Example Push Data:
            {
                "arg": {
                    "channel": "account"
                },
                "data": {
                    "ts": "1597026383085",
                    "totalEquity": "41624.32",
                    "isolatedEquity": "3624.32",
                    "details": [{
                        "currency": "USDT",
                        "equity": "1",
                        "balance": "1",
                        "ts": "1617279471503",
                        "isolatedEquity": "0",
                        "equityUsd": "45078.3790756226851775",
                        "availableEquity": "1",
                        "available": "0",
                        "frozen": "0",
                        "orderFrozen": "0",
                        "unrealizedPnl": "0",
                        "isolatedUnrealizedPnl": "0"
                    }]
                }
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
        """
        return await self.subscribe("account")
        
    async def subscribeAlgoOrders(self, instId: Optional[str] = None) -> bool:
        """Subscribe to algo orders channel (includes trigger orders and TP/SL orders).
        Data will only be pushed when there are order updates.
        
        Args:
            instId: Optional instrument ID. If None, subscribes to all instruments.
            
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            action: Push data type ("snapshot" for full, "update" for incremental)
            data: Array of algo order information containing:
                instId: Instrument ID
                instType: Instrument type
                algoId: Algo order ID
                clientOrderId: Client-assigned order ID
                size: Order quantity
                orderType: Order type
                    - "conditional": One-way stop order
                    - "trigger": Trigger order
                side: Order side ("buy" or "sell")
                positionSide: Position side
                marginMode: Margin mode
                leverage: Position leverage
                state: Order state
                    - "live": To be effective
                    - "effective": Effective
                    - "canceled": Canceled
                    - "order_failed": Order failed
                tpTriggerPrice: Take-profit trigger price
                tpOrderPrice: Take-profit order price (-1 for market price)
                slTriggerPrice: Stop-loss trigger price
                slOrderPrice: Stop-loss order price (-1 for market price)
                triggerPrice: Trigger price for trigger orders
                triggerPriceType: Price type for triggers ("last"/"index"/"mark")
                orderPrice: Order price for trigger orders
                actualSize: Actual order quantity
                actualSide: Actual order side ("tp"/"sl", for conditional orders)
                reduceOnly: Whether order only reduces position size
                cancelType: Cancel source ("not_canceled"/"user_canceled"/"system_canceled")
                createTime: Creation time in milliseconds
                updateTime: Update time in milliseconds
                brokerId: Broker ID (up to 16 characters)
                attachAlgoOrders: Array of attached TP/SL orders containing:
                    tpTriggerPrice: Take-profit trigger price
                    tpTriggerPriceType: Take-profit trigger price type
                    tpOrderPrice: Take-profit order price (-1 for market)
                    slTriggerPrice: Stop-loss trigger price
                    slTriggerPriceType: Stop-loss trigger price type
                    slOrderPrice: Stop-loss order price (-1 for market)
            
        Example of push data:
            {
                "action": "snapshot",
                "arg": {
                    "channel": "orders-algo"
                },
                "data": [{
                    "instType": "SWAP",
                    "instId": "BTC-USDT",
                    "algoId": "11779982",
                    "clientOrderId": "",
                    "size": "100",
                    "orderType": "conditional",
                    "side": "buy",
                    "positionSide": "long",
                    "marginMode": "cross",
                    "leverage": "10",
                    "state": "live",
                    "tpTriggerPrice": "73000",
                    "tpOrderPrice": "-1",
                    "triggerPriceType": "last",
                    "reduceOnly": "false",
                    "cancelType": "not_canceled",
                    "createTime": "1731056529341",
                    "updateTime": "1731056529341",
                    "attachAlgoOrders": [{
                        "tpTriggerPrice": "75000",
                        "tpTriggerPriceType": "market",
                        "tpOrderPrice": "-1"
                    }]
                }]
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
            No data will be pushed when first subscribed.
        """
        return await self.subscribe("orders-algo", instId)

class BlofinWsCopytradingClient(BlofinWsClient):
    """BloFin copytrading WebSocket API client.
    Example: 
        ```python
        async with BlofinWsCopytradingClient(apiKey, secret, passphrase) as client:
            await client.connect()
            await client.subscribeCopytradingPositions()
            async for message in client.listen():
                print(message)  # Process each message
        ```  
    """
    
    def __init__(self, apiKey: str, secret: str, passphrase: str):
        """Initialize copytrading WebSocket client.
        
        Args:
            apiKey: API access key
            secret: API secret key
            passphrase: API passphrase
        """
        super().__init__(apiKey=apiKey, secret=secret, passphrase=passphrase, isCopytrading=True)
        
    async def subscribeCopytradingPositions(self) -> bool:
        """Subscribe to copytrading positions channel. Initial snapshot will be pushed on subscription.
        Data will be pushed on events (order placement/cancellation) and at regular intervals.
        
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            data: Array of position information containing:
                instId: Instrument ID (e.g. "BTC-USDT")
                instType: Instrument type
                marginMode: Margin mode ("cross" or "isolated")
                positionId: Position ID
                positionSide: Position side ("long", "short", or "net")
                    Note: For "net", positive means long, negative means short
                positions: Quantity of positions
                availablePositions: Position that can be closed
                averagePrice: Average open price
                unrealizedPnl: Unrealized profit and loss (mark price)
                unrealizedPnlRatio: Unrealized profit and loss ratio
                leverage: Position leverage
                liquidationPrice: Estimated liquidation price
                markPrice: Latest mark price
                initialMargin: Initial margin requirement (cross mode only)
                margin: Margin (can be added or reduced)
                marginRatio: Margin ratio
                maintenanceMargin: Maintenance margin requirement
                adl: Auto decrease line level (1-5, lower means weaker)
                createTime: Creation time in milliseconds
                updateTime: Latest adjustment time in milliseconds
                attachTpsls: Attached TP/SL orders containing:
                    tpTriggerPrice: Take-profit trigger price
                    tpTriggerPriceType: Take-profit trigger price type ("last")
                    tpOrderPrice: Take-profit order price (-1 for market)
                    slTriggerPrice: Stop-loss trigger price
                    slTriggerPriceType: Stop-loss trigger price type ("last")
                    slOrderPrice: Stop-loss order price (-1 for market)
                    size: Order quantity (-1 for entire position)
            
        Example of push data:
            {
                "arg": {
                    "channel": "copytrading-positions"
                },
                "data": [{
                    "instType": "SWAP",
                    "instId": "BNB-USDT",
                    "marginMode": "cross",
                    "positionId": "8138",
                    "positionSide": "net",
                    "positions": "-100",
                    "availablePositions": "-100",
                    "averagePrice": "130.06",
                    "unrealizedPnl": "-77.1",
                    "unrealizedPnlRatio": "-1.778409964631708442",
                    "leverage": "3",
                    "liquidationPrice": "107929.699398660166170462",
                    "markPrice": "207.16",
                    "initialMargin": "69.053333333333333333",
                    "margin": "",
                    "marginRatio": "131.337873621866389829",
                    "maintenanceMargin": "1.0358",
                    "adl": "3",
                    "createTime": "1695795726481",
                    "updateTime": "1695795726484",
                    "attachTpsls": {
                        "tpTriggerPrice": "75000",
                        "tpTriggerPriceType": "last",
                        "tpOrderPrice": "-1",
                        "size": "-1"
                    }
                }]
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
        """
        return await self.subscribe("copytrading-positions")
        
    async def subscribeCopytradingOrders(self) -> bool:
        """Subscribe to copytrading orders channel. Data will only be pushed when there
        are order updates.
        
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            action: Push data type ("snapshot" for full, "update" for incremental)
            data: Array of order information containing:
                instId: Instrument ID (e.g. "BTC-USDT")
                instType: Instrument type
                orderId: Order ID
                price: Order price
                size: Number of contracts
                orderType: Order type
                side: Order side
                positionSide: Position side
                marginMode: Margin mode
                filledSize: Accumulated fill quantity
                filledAmount: Filled amount
                averagePrice: Average filled price (empty if not filled)
                state: Order state
                leverage: Position leverage
                tpTriggerPrice: Take-profit trigger price
                tpOrderPrice: Take-profit order price (-1 for market)
                slTriggerPrice: Stop-loss trigger price
                slOrderPrice: Stop-loss order price (-1 for market)
                fee: Fee and rebate
                pnl: Profit and loss (for closing orders)
                cancelSource: Cancel source
                orderCategory: Order category:
                    - "normal": Normal order
                    - "full_liquidation": Full liquidation
                    - "partial_liquidation": Partial liquidation
                    - "adl": ADL order
                    - "tp": Take-profit order
                    - "sl": Stop-loss order
                createTime: Creation time in milliseconds
                updateTime: Update time in milliseconds
                brokerId: Broker ID (up to 16 characters)
            
        Example of push data:
            {
                "arg": {
                    "channel": "copytrading-orders"
                },
                "data": [{
                    "instType": "SWAP",
                    "instId": "BTC-USDT",
                    "orderId": "28334314",
                    "price": "28000.000000000000000000",
                    "size": "10",
                    "orderType": "limit",
                    "side": "sell",
                    "positionSide": "net",
                    "marginMode": "cross",
                    "filledSize": "0",
                    "filledAmount": "0.000000000000000000",
                    "averagePrice": "0.000000000000000000",
                    "state": "live",
                    "leverage": "2",
                    "tpTriggerPrice": "27000.000000000000000000",
                    "tpOrderPrice": "-1",
                    "slTriggerPrice": null,
                    "slOrderPrice": null,
                    "fee": "0.000000000000000000",
                    "pnl": "0.000000000000000000",
                    "cancelSource": "",
                    "orderCategory": "pre_tp_sl",
                    "createTime": "1696760245931",
                    "updateTime": "1696760245973"
                }]
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
            No data will be pushed when first subscribed.
        """
        return await self.subscribe("copytrading-orders")
        
    async def subscribeCopytradingSubPositions(self) -> bool:
        """Subscribe to copytrading sub-positions channel. Initial snapshot will be pushed on subscription.
        Data will be pushed on events (order placement/cancellation) and at regular intervals.
        
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            data: Array of position information containing:
                instId: Instrument ID (e.g. "BTC-USDT")
                instType: Instrument type
                marginMode: Margin mode ("cross" or "isolated")
                positionId: Position ID
                positionSide: Position side ("long", "short", or "net")
                    Note: For "net", positive means long, negative means short
                positions: Quantity of positions
                availablePositions: Position that can be closed
                averagePrice: Average open price
                unrealizedPnl: Unrealized profit and loss (mark price)
                unrealizedPnlRatio: Unrealized profit and loss ratio
                leverage: Position leverage
                liquidationPrice: Estimated liquidation price
                markPrice: Latest mark price
                initialMargin: Initial margin requirement (cross mode only)
                margin: Margin (can be added or reduced)
                marginRatio: Margin ratio
                maintenanceMargin: Maintenance margin requirement
                adl: Auto decrease line level (1-5, lower means weaker)
                createTime: Creation time in milliseconds
                updateTime: Latest adjustment time in milliseconds
                attachTpsls: Attached TP/SL orders containing:
                    tpTriggerPrice: Take-profit trigger price
                    tpTriggerPriceType: Take-profit trigger price type ("last")
                    tpOrderPrice: Take-profit order price (-1 for market)
                    slTriggerPrice: Stop-loss trigger price
                    slTriggerPriceType: Stop-loss trigger price type ("last")
                    slOrderPrice: Stop-loss order price (-1 for market)
                    size: Order quantity (-1 for entire position)
            
        Example of push data:
            {
                "arg": {
                    "channel": "copytrading-sub-positions"
                },
                "data": [{
                    "instType": "SWAP",
                    "instId": "BNB-USDT",
                    "marginMode": "cross",
                    "positionId": "8138",
                    "positionSide": "net",
                    "positions": "-100",
                    "availablePositions": "-100",
                    "averagePrice": "130.06",
                    "unrealizedPnl": "-77.1",
                    "unrealizedPnlRatio": "-1.778409964631708442",
                    "leverage": "3",
                    "liquidationPrice": "107929.699398660166170462",
                    "markPrice": "207.16",
                    "initialMargin": "69.053333333333333333",
                    "margin": "",
                    "marginRatio": "131.337873621866389829",
                    "maintenanceMargin": "1.0358",
                    "adl": "3",
                    "createTime": "1695795726481",
                    "updateTime": "1695795726484",
                    "attachTpsls": {
                        "tpTriggerPrice": "75000",
                        "tpTriggerPriceType": "last",
                        "tpOrderPrice": "-1",
                        "size": "-1"
                    }
                }]
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
        """
        return await self.subscribe("copytrading-sub-positions")
        
    async def subscribeCopytradingAccount(self) -> bool:
        """Subscribe to copytrading account channel. Data will be pushed on events (order placement,
        cancellation, execution) and at regular intervals.
        
        Returns:
            bool: True if subscription successful
            
        Push Data Parameters:
            data: Account information containing:
                ts: Update time in milliseconds
                totalEquity: Total equity in USD
                isolatedEquity: Isolated margin equity in USD
                details: Array of currency details, each containing:
                    currency: Currency name
                    equity: Currency equity
                    balance: Cash balance
                    ts: Currency balance update time in milliseconds
                    isolatedEquity: Isolated margin equity in this currency
                    available: Available balance
                    availableEquity: Available equity
                    frozen: Frozen balance
                    orderFrozen: Margin frozen for open orders
                    equityUsd: Equity in USD
                    isolatedUnrealizedPnl: Isolated unrealized profit/loss
                    coinUsdPrice: Price index USD of currency
                    spotAvailable: Spot balance of the currency
                    liability: Liabilities of currency (Multi-currency margin)
                    borrowFrozen: Potential borrowing IMR in USD (Multi-currency margin)
                    marginRatio: Cross maintenance margin requirement (Multi-currency margin)
            
        Example of push data:
            {
                "arg": {
                    "channel": "copytrading-account"
                },
                "data": {
                    "ts": "1597026383085",
                    "totalEquity": "41624.32",
                    "isolatedEquity": "3624.32",
                    "details": [{
                        "currency": "USDT",
                        "equity": "1",
                        "balance": "1",
                        "ts": "1617279471503",
                        "isolatedEquity": "0",
                        "equityUsd": "45078.3790756226851775",
                        "availableEquity": "1",
                        "available": "0",
                        "frozen": "0",
                        "orderFrozen": "0",
                        "unrealizedPnl": "0",
                        "isolatedUnrealizedPnl": "0"
                    }]
                }
            }
            
        Note:
            This channel requires authentication and uses private WebSocket.
        """
        return await self.subscribe("copytrading-account")
