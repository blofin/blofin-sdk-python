"""BloFin API exceptions."""

from typing import Optional, Dict, Union

class BlofinAPIException(Exception):
    """Base exception class for BloFin API errors.
    
    Attributes:
        message: Error message
        status_code: HTTP status code
        response: Full response data
        code: Error code from API response
        data: Additional error data from API response
    """
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Union[Dict, str]] = None,
        code: Optional[str] = None,
        data: Optional[Dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        self.code = code
        self.data = data or {}
        super().__init__(self.message)
