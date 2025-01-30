import base64
import hmac
import json
import time
from hashlib import sha256
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode
from blofin.exceptions import BlofinAPIException

import requests
import websockets
import asyncio
import threading


class BaseClient:
    """Base class for BloFin API clients."""
    
    def __init__(
        self,
        apiKey: Optional[str] = None,
        apiSecret: Optional[str] = None,
        passphrase: Optional[str] = None,
        useServerTime: bool = False,
        baseUrl: str = "https://openapi.blofin.com",
        timeout: float = 30.0,
        proxies: Optional[Dict] = None
    ):
        self.API_KEY = apiKey
        self.API_SECRET = apiSecret.encode('utf-8') if apiSecret else None
        self.PASSPHRASE = passphrase
        self.use_server_time = useServerTime
        self.base_url = baseUrl
        self.timeout = timeout
        self.proxies = proxies or {}
        self.session = requests.Session()

    def _get_timestamp(self) -> str:
        if self.use_server_time:
            return self._get_server_timestamp()
        return str(int(time.time() * 1000))

    def _get_server_timestamp(self) -> str:
        response = requests.get(f"{self.base_url}/api/v1/public/time")
        if response.status_code == 200:
            return response.json()['data']['ts']
        return str(int(time.time() * 1000))

    def _get_nonce(self) -> str:
        return str(int(time.time() * 1000))

    def _sign_request(
        self,
        timestamp: str,
        method: str,
        request_path: str,
        body: Union[Dict, List, str, None] = None,
        nonce: Optional[str] = None
    ) -> str:
        if body is None:
            body = ""
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
            
        if nonce is None:
            nonce = self._get_nonce()
            
        prehash = request_path + method.upper() + timestamp + nonce + (body or "")
        
        mac = hmac.new(
            self.API_SECRET,
            prehash.encode('utf-8'),
            digestmod=sha256
        )
        
        hex_signature = mac.hexdigest()
        
        return base64.b64encode(hex_signature.encode('utf-8')).decode('utf-8')

    def _handle_response(self, response: requests.Response) -> Dict:
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
        method = method.upper()
        
        url = self.base_url + path
        if params:
            url += '?' + urlencode(params)
            
        headers = {'Content-Type': 'application/json'}
        
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
        return self._request('GET', path, params=params, sign=sign)

    def post(self, path: str, data: Optional[Dict] = None, sign: bool = True) -> Dict:
        return self._request('POST', path, data=data, sign=sign)


class Client(BaseClient):
    """BloFin API HTTP client for production environment."""
    
    def __init__(
        self,
        apiKey: Optional[str] = None,
        apiSecret: Optional[str] = None,
        passphrase: Optional[str] = None,
        useServerTime: bool = False,
        baseUrl: str = "https://openapi.blofin.com",
        timeout: float = 30.0,
        proxies: Optional[Dict] = None,
        isDemo: bool = False
    ):
        """Initialize the client.
        
        Args:
            apiKey: BloFin API key, required for authenticated endpoints
            apiSecret: BloFin API secret, required for authenticated endpoints
            passphrase: BloFin API passphrase, required for authenticated endpoints
            useServerTime: Whether to use server time for requests
            baseUrl: API base URL, use demo URL for testing
            timeout: Request timeout in seconds
            proxies: Optional proxy configuration for requests
            isDemo: If True, use demo trading endpoints
        """
        if isDemo:
            baseUrl = "https://demo-trading-openapi.blofin.com"
            
        super().__init__(
            apiKey=apiKey,
            apiSecret=apiSecret,
            passphrase=passphrase,
            useServerTime=useServerTime,
            baseUrl=baseUrl,
            timeout=timeout,
            proxies=proxies
        )
        self.is_demo = isDemo


class DemoClient(Client):
    """BloFin API HTTP client for demo trading environment."""
    
    def __init__(
        self,
        apiKey: Optional[str] = None,
        apiSecret: Optional[str] = None,
        passphrase: Optional[str] = None,
        useServerTime: bool = False,
        timeout: float = 30.0,
        proxies: Optional[Dict] = None
    ):
        """Initialize demo trading client.
        
        Args:
            apiKey: BloFin API key, required for authenticated endpoints
            apiSecret: BloFin API secret, required for authenticated endpoints
            passphrase: BloFin API passphrase, required for authenticated endpoints
            useServerTime: Whether to use server time for requests
            timeout: Request timeout in seconds
            proxies: Optional proxy configuration for requests
        """
        super().__init__(
            apiKey=apiKey,
            apiSecret=apiSecret,
            passphrase=passphrase,
            useServerTime=useServerTime,
            timeout=timeout,
            proxies=proxies,
            isDemo=True
        )
