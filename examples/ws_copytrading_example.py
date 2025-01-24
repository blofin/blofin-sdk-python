import asyncio
import json
from blofin.websocket_client import BlofinWsCopytradingClient

async def main():
    # Initialize copytrading websocket client
    # Replace with your own API key, secret and passphrase
    client = BlofinWsCopytradingClient(
        apiKey="....",
        secret="....",
        passphrase="...."
    )

    try:
        # Connect to websocket server
        print("Connecting to websocket server...")
        await client.connect()
        print("Connected successfully!")

        # Subscribe to copytrading orders
        print("Subscribing to copytrading orders...")
        await client.subscribeCopytradingOrders()
        print("Subscribed to copytrading orders")

        # Subscribe to copytrading positions
        print("Subscribing to copytrading positions...")
        await client.subscribeCopytradingPositions()
        print("Subscribed to copytrading positions")
        await client.subscribeCopytradingSubPositions()
        print("Subscribed to copytrading sub positions")
        await client.subscribeCopytradingAccount()
        print("Subscribed to copytrading account")

        # Listen for messages
        print("Listening for messages...")
        async for message in client.listen():
            print(f"Received message: {json.dumps(message, indent=2)}")

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close websocket connection
        await client.close()
        print("Connection closed")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
