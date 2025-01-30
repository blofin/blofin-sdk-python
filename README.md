# BloFin SDK Package

Python SDK for interacting with the BloFin API.

## Installation

```bash
pip install -e .
```

## Quick Start

### REST API

```python
from blofin.client import Client, DemoClient
from blofin.rest_trading import TradingAPI
from blofin.rest_market import MarketAPI
from blofin.rest_affiliate import AffiliateAPI
from blofin.rest_copytrading import CopyTradingAPI

# Initialize production client
client = Client(
    apiKey="your-api-key",
    apiSecret="your-api-secret",
    passphrase="your-passphrase"
)

# Or initialize demo trading client
demo_client = DemoClient(
    apiKey="your-api-key",
    apiSecret="your-api-secret",
    passphrase="your-passphrase"
)

# Initialize APIs (works with both production and demo clients)
trading = TradingAPI(client)  # or TradingAPI(demo_client)
market = MarketAPI(client)    # or MarketAPI(demo_client)
affiliate = AffiliateAPI(client)  # or AffiliateAPI(demo_client)
copytrading = CopyTradingAPI(client)  # or CopyTradingAPI(demo_client)
```

### WebSocket API

```python
from blofin.websocket_client import BlofinWsClient, BlofinWsPublicClient, BlofinWsPrivateClient, BlofinWsCopytradingClient

# Public WebSocket (no authentication required)
public_client = BlofinWsPublicClient()  # For production
demo_public_client = BlofinWsPublicClient(isDemo=True)  # For demo trading

# Private WebSocket (authentication required)
private_client = BlofinWsPrivateClient(
    apiKey="your-api-key",
    secret="your-api-secret",
    passphrase="your-passphrase"
)  # For production

demo_private_client = BlofinWsPrivateClient(
    apiKey="your-api-key",
    secret="your-api-secret",
    passphrase="your-passphrase",
    isDemo=True
)  # For demo trading

# Copytrading WebSocket
copytrading_client = BlofinWsCopytradingClient(
    apiKey="your-api-key",
    secret="your-api-secret",
    passphrase="your-passphrase"
)  # For production

```

For detailed usage examples, please refer to the [examples](examples/) directory.

## Demo Trading Environment

BloFin provides a demo trading environment for testing and development. To use the demo environment:

1. **REST API**:
   - Use the `DemoClient` class instead of `Client`
   - Or set `isDemo=True` when initializing a regular `Client`
   - Demo trading base URL: `https://demo-trading-openapi.blofin.com`

2. **WebSocket API**:
   - Set `isDemo=True` when initializing WebSocket clients
   - Demo WebSocket URLs:
     - Public: `wss://demo-trading-openapi.blofin.com/ws/public`
     - Private: `wss://demo-trading-openapi.blofin.com/ws/private`

3. **Features**:
   - Test trading strategies without real funds
   - Same API interface as production
   - Simulated market conditions
   - Practice risk management

## Documentation

For detailed API documentation, please refer to the [BloFin API Documentation](https://blofin.com/docs).

## Features

### REST API
- Account management
- Trading operations
- Position management
- Order management
- Asset operations
- Market data
- Affiliate system
- Copytrading

### WebSocket API
- Real-time market data
- Real-time order updates
- Real-time position updates
- Real-time account updates
- Copytrading functionality

## Testing

Run the test suite:

```bash
python -m pytest
```

## License

This project is licensed under the Apache License.

## Security

Never share your API credentials. Always store them securely and never commit them to version control.
