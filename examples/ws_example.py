import asyncio
import logging
import sys
import json

from blofin.websocket_client import BlofinWsPrivateClient, BlofinWsPublicClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API credentials
blofinApiKey = "...."
blofinSecret = "...."
blofinPassphrase = "...."

async def handleMessages(ws, name: str):
    """Handle messages from WebSocket channels."""
    async for msg in ws.listen():
        print(f"{name} channel message:", json.dumps(msg, indent=2))

async def main():
    # Initialize clients
    privateWs = BlofinWsPrivateClient(
        apiKey=blofinApiKey,
        secret=blofinSecret,
        passphrase=blofinPassphrase
    )
    publicWs = BlofinWsPublicClient()
    
    try:
        # Connect to WebSocket servers
        logger.info("Connecting to private WebSocket...")
        await privateWs.connect()
        logger.info("Private WebSocket connected")
        
        logger.info("Connecting to public WebSocket...")
        await publicWs.connect()
        logger.info("Public WebSocket connected")
        
        # Subscribe to channels
        logger.info("Subscribing to private channels...")
        await privateWs.subscribeOrders()
        #await privateWs.subscribeAlgoOrders()
        #await privateWs.subscribePositions()
        await privateWs.subscribeAccount()
        
        logger.info("Subscribing to public channels...")
        #await publicWs.subscribeTrades(instId="BTC-USDT")
        #await publicWs.subscribeOrderBook(instId="ETH-USDT", depth="books5")
        #await publicWs.subscribeTickers(instId="BTC-USDT")

        
        print("WebSocket connected and subscribed. Press Ctrl+C to exit.")
        
        # Create tasks for message handlers
        privateHandler = asyncio.create_task(handleMessages(privateWs, "Private"))
        publicHandler = asyncio.create_task(handleMessages(publicWs, "Public"))
        
        # Wait for handlers to complete
        await asyncio.gather(privateHandler, publicHandler)
            
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await privateWs.close()
        await publicWs.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Program exited cleanly")
