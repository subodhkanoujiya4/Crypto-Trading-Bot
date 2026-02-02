"""
Binance Futures Testnet Client Wrapper
Handles API authentication and communication with Binance Futures Testnet
"""

import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class BinanceClient:
    """
    Client for interacting with Binance Futures Testnet API
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize Binance client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key
        })
        
        logger.info(f"Initialized BinanceClient with base URL: {self.base_url}")
    
    def _generate_signature(self, params: Dict) -> str:
        """
        Generate HMAC SHA256 signature for API request
        
        Args:
            params: Request parameters
            
        Returns:
            HMAC signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Dict:
        """
        Make HTTP request to Binance API
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether request requires signature
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.exceptions.RequestException: On network errors
            ValueError: On API errors
        """
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        logger.debug(f"Making {method} request to {endpoint}")
        logger.debug(f"Parameters: {params}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method == 'POST':
                response = self.session.post(url, params=params, timeout=10)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            # Check for HTTP errors
            if response.status_code != 200:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('msg', 'Unknown error')
                error_code = error_data.get('code', 'N/A')
                raise ValueError(f"API Error [{error_code}]: {error_msg}")
            
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Connection error occurred")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise
    
    def test_connectivity(self) -> bool:
        """
        Test connection to Binance API
        
        Returns:
            True if connection successful
        """
        try:
            self._request('GET', '/fapi/v1/ping')
            logger.info("Connectivity test successful")
            return True
        except Exception as e:
            logger.error(f"Connectivity test failed: {str(e)}")
            return False
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict:
        """
        Get exchange trading rules and symbol information
        
        Args:
            symbol: Optional symbol to filter
            
        Returns:
            Exchange info dictionary
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        return self._request('GET', '/fapi/v1/exchangeInfo', params=params)
    
    def get_account_info(self) -> Dict:
        """
        Get account information
        
        Returns:
            Account info dictionary
        """
        return self._request('GET', '/fapi/v2/account', signed=True)
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: Optional[float] = None,
                   time_in_force: str = 'GTC') -> Dict:
        """
        Place an order on Binance Futures
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (default: GTC - Good Till Cancel)
            
        Returns:
            Order response dictionary
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        logger.info(f"Placing {order_type} {side} order: {quantity} {symbol} @ {price if price else 'MARKET'}")
        
        response = self._request('POST', '/fapi/v1/order', params=params, signed=True)
        
        logger.info(f"Order placed successfully. Order ID: {response.get('orderId')}")
        
        return response
    
    def get_order(self, symbol: str, order_id: int) -> Dict:
        """
        Query order status
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Order details dictionary
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        return self._request('GET', '/fapi/v1/order', params=params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an active order
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Cancellation response dictionary
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Cancelling order {order_id} for {symbol}")
        
        return self._request('DELETE', '/fapi/v1/order', params=params, signed=True)
