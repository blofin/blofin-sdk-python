# BloFin SDK Package

Python SDK for interacting with the BloFin API.

## Installation

```bash
pip install -e .
```

## Quick Start

### REST API

```python
from blofin.client import Client
from blofin.rest_trading import TradingAPI
from blofin.rest_market import MarketAPI
from blofin.rest_affiliate import AffiliateAPI
from blofin.rest_copytrading import CopyTradingAPI

# Initialize client
client = Client(
    api_key="your-api-key",
    api_secret="your-api-secret",
    passphrase="your-passphrase"
)

# Initialize APIs
trading = TradingAPI(client)
market = MarketAPI(client)
affiliate = AffiliateAPI(client)
copytrading = CopyTradingAPI(client)
```

### WebSocket API

```python
from blofin.websocket_client import BlofinWsClient, BlofinWsPublicClient, BlofinWsPrivateClient, BlofinWsCopytradingClient

# Public WebSocket (no authentication required)
public_client = BlofinWsPublicClient()

# Private WebSocket (authentication required)
private_client = BlofinWsPrivateClient(
    apiKey="your-api-key",
    secret="your-api-secret",
    passphrase="your-passphrase"
)

# Copytrading WebSocket
copytrading_client = BlofinWsCopytradingClient(
    apiKey="your-api-key",
    secret="your-api-secret",
    passphrase="your-passphrase"
)
```

For detailed usage examples, please refer to the [examples](examples/) directory.

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

This project is licensed under the Apache License 

## Security

Never share your API credentials. Always store them securely and never commit them to version control.
