"""BloFin Python SDK.

Public entry point for the package. Importing from the package root keeps
call sites stable even if the internal module layout changes, so this module
re-exports the documented public API surface:

    from blofin import Client, DemoClient, TradingAPI, MarketAPI

All names below are considered part of the supported public API. Anything not
re-exported here is an internal implementation detail and may change without
a major version bump.
"""

from blofin.client import BaseClient, Client, DemoClient
from blofin.exceptions import BlofinAPIException
from blofin.logger_config import configure_logging, get_logger
from blofin.rest_affiliate import AffiliateAPI
from blofin.rest_copytrading import CopyTradingAPI
from blofin.rest_market import MarketAPI
from blofin.rest_trading import TradingAPI
from blofin.websocket_client import (
    BlofinWsClient,
    BlofinWsCopytradingClient,
    BlofinWsPrivateClient,
    BlofinWsPublicClient,
)

__version__ = "0.1.0"

__all__ = [
    "AffiliateAPI",
    "BaseClient",
    "BlofinAPIException",
    "BlofinWsClient",
    "BlofinWsCopytradingClient",
    "BlofinWsPrivateClient",
    "BlofinWsPublicClient",
    "Client",
    "CopyTradingAPI",
    "DemoClient",
    "MarketAPI",
    "TradingAPI",
    "configure_logging",
    "get_logger",
]