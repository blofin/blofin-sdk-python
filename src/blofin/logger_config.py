"""Logging configuration for BloFin SDK."""

import logging
import os
from typing import Optional

# Default format includes timestamp, level, logger name, and message
DEFAULT_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"

# Get log level from environment variable, default to INFO
DEFAULT_LOG_LEVEL = os.environ.get("BLOFIN_LOG_LEVEL", "INFO").upper()

def configure_logging(level: Optional[str] = None, format_str: Optional[str] = None):
    """Configure global logging settings for BloFin SDK.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_str: Custom log format string
    """
    log_level = (level or DEFAULT_LOG_LEVEL).upper()
    if not hasattr(logging, log_level):
        log_level = "INFO"
        
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=format_str or DEFAULT_FORMAT
    )

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a component.
    
    Args:
        name: Logger name (e.g., 'rest', 'websocket', 'utils')
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"blofin.{name}")

# Configure logging with default settings
configure_logging()

# Create module-level logger
logger = get_logger("core")
logger.debug("BloFin SDK logging configured")
