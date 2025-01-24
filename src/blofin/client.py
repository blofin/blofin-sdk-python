import base64
import hmac
import json
import time
from hashlib import sha256
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode
from blofin.exceptions import BlofinAPIException

import requests


class Client:
    """BloFin API HTTP client.
    
    Handles HTTP requests to the BloFin API including authentication, request signing,
    and response processing.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        passphrase: Optional[str] = None,
        use_server_time: bool = False,
        base_url: str = "https://openapi.blofin.com",
        timeout: float = 30.0,
        proxies: Optional[Dict] = None
    ):
        """Initialize the client.
        
        Args:
            api_key: BloFin API key, required for authenticated endpoints
            api_secret: BloFin API secret, required for authenticated endpoints
            passphrase: BloFin API passphrase, required for authenticated endpoints
            use_server_time: Whether to use server time for requests
            base_url: API base URL, use demo URL for testing
            timeout: Request timeout in seconds
            proxies: Optional proxy configuration for requests
        """
        self.API_KEY = api_key
        self.API_SECRET = api_secret.encode('utf-8') if api_secret else None
        self.PASSPHRASE = passphrase
        self.use_server_time = use_server_time
        self.base_url = base_url
        self.timeout = timeout
        self.proxies = proxies or {}
        self.session = requests.Session()

    def _get_timestamp(self) -> str:
        """Get current timestamp in milliseconds.
        
        If use_server_time is True, will sync with server time.
        
        Returns:
            Current timestamp as string
        """
        if self.use_server_time:
            return self._get_server_timestamp()
        return str(int(time.time() * 1000))

    def _get_server_timestamp(self) -> str:
        """Get server timestamp.
        
        Makes request to server time endpoint to sync timestamp.
        
        Returns:
            Server timestamp as string
        """
        response = requests.get(f"{self.base_url}/api/v1/public/time")
        if response.status_code == 200:
            return response.json()['data']['ts']
        return str(int(time.time() * 1000))

    def _get_nonce(self) -> str:
        """Get unique nonce value.
        
        Returns:
            Current timestamp as nonce
        """
        return str(int(time.time() * 1000))

    def _sign_request(
        self,
        timestamp: str,
        method: str,
        request_path: str,
        body: Union[Dict, List, str, None] = None,
        nonce: Optional[str] = None
    ) -> str:
        """Generate signed request headers.
        
        Args:
            timestamp: Request timestamp
            method: HTTP method
            request_path: Request path
            body: Request body for POST requests
            nonce: Unique identifier for request
            
        Returns:
            Base64 encoded signature
        """
        if body is None:
            body = ""
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
            
        if nonce is None:
            nonce = self._get_nonce()
            
        # Create prehash string
        prehash = request_path + method.upper() + timestamp + nonce + (body or "")
        
        # Generate HMAC-SHA256 signature
        mac = hmac.new(
            self.API_SECRET,
            prehash.encode('utf-8'),
            digestmod=sha256
        )
        
        # Convert to hex string
        hex_signature = mac.hexdigest()
        
        # Encode hex string as bytes then to base64
        return base64.b64encode(hex_signature.encode('utf-8')).decode('utf-8')

    def _handle_response(self, response: requests.Response) -> Dict:
        """Process API response.
        
        Args:
            response: Response from API
            
        Returns:
            Parsed response data
            
        Raises:
            BlofinAPIException: If response indicates an error
        """
        try:
            response_data = response.json()
            error_code = response_data.get('code')
            error_msg = response_data.get('msg')
            error_data = response_data.get('data')
            if response.status_code != 200 or error_code != '0':
                raise BlofinAPIException(
                    message=f"API request failed: {error_msg}",
                    status_code=response.status_code,
                    response=response_data,
                    code=str(error_code),
                    data=error_data
                )
            return response_data
        except ValueError as e:
            raise BlofinAPIException(
                message=f"Invalid JSON response: {e}",
                status_code=response.status_code,
                response=response.text
            )

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        sign: bool = True
    ) -> Dict:
        """Make request to BloFin API.
        
        Args:
            method: HTTP method (GET/POST)
            path: API endpoint path
            params: URL parameters for GET requests
            data: Request body for POST requests
            sign: Whether to sign the request. Set to False for public endpoints
            
        Returns:
            Parsed response data
        """
        method = method.upper()
        
        # Build URL
        url = self.base_url + path
        if params:
            url += '?' + urlencode(params)
            
        # Prepare headers
        headers = {'Content-Type': 'application/json'}
        
        # Add authentication headers for private endpoints
        if sign:
            if not all([self.API_KEY, self.API_SECRET, self.PASSPHRASE]):
                raise BlofinAPIException(
                    message="API key, secret and passphrase are required for authenticated endpoints",
                    status_code=None,
                    response=None
                )
                
            timestamp = self._get_timestamp()
            nonce = self._get_nonce()
            signature = self._sign_request(
                timestamp,
                method,
                path + ('?' + urlencode(params) if params else ''),
                data,
                nonce
            )
            
            headers.update({
                'ACCESS-KEY': self.API_KEY,
                'ACCESS-SIGN': signature,
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-NONCE': nonce,
                'ACCESS-PASSPHRASE': self.PASSPHRASE
            })
        
        # Make request
        try:
            response = self.session.request(
                method,
                url,
                headers=headers,
                json=data if data else None,
                timeout=self.timeout,
                proxies=self.proxies
            )
            response_data = response.json()
            if response.status_code != 200:
                raise BlofinAPIException(
                    message=f"API request failed with status code {response.status_code}",
                    status_code=response.status_code,
                    response=response_data
                )
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise BlofinAPIException(
                message=f"Request failed: {str(e)}",
                status_code=None,
                response=None
            )

    def get(self, path: str, params: Optional[Dict] = None, sign: bool = True) -> Dict:
        """Send GET request.
        
        Args:
            path: API endpoint path
            params: URL parameters
            sign: Whether to sign the request. Set to False for public endpoints
            
        Returns:
            Parsed response data
        """
        return self._request('GET', path, params=params, sign=sign)

    def post(self, path: str, data: Optional[Dict] = None, sign: bool = True) -> Dict:
        """Send POST request.
        
        Args:
            path: API endpoint path
            data: Request body data
            sign: Whether to sign the request. Set to False for public endpoints
            
        Returns:
            Parsed response data
        """
        return self._request('POST', path, data=data, sign=sign)
