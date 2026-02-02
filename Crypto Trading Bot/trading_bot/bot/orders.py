"""
Order Management Module
Handles order placement and management logic
"""

from typing import Dict, Optional
import logging
from .client import BinanceClient
from .validators import OrderValidator, ValidationError

logger = logging.getLogger(__name__)


class OrderManager:
    """
    Manages order placement and tracking
    """
    
    def __init__(self, client: BinanceClient):
        """
        Initialize OrderManager
        
        Args:
            client: BinanceClient instance
        """
        self.client = client
        self.validator = OrderValidator()
        logger.info("OrderManager initialized")
    
    def place_order(self, symbol: str, side: str, order_type: str,
                   quantity: str, price: Optional[str] = None) -> Dict:
        """
        Validate and place an order
        
        Args:
            symbol: Trading symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Order response dictionary
            
        Raises:
            ValidationError: If parameters are invalid
            Exception: If order placement fails
        """
        # Validate all parameters
        try:
            validated_symbol, validated_side, validated_order_type, \
            validated_quantity, validated_price = self.validator.validate_order_params(
                symbol, side, order_type, quantity, price
            )
        except ValidationError as e:
            logger.error(f"Parameter validation failed: {str(e)}")
            raise
        
        # Print order summary
        self._print_order_summary(
            validated_symbol,
            validated_side,
            validated_order_type,
            validated_quantity,
            validated_price
        )
        
        # Place the order
        try:
            logger.info("Attempting to place order...")
            response = self.client.place_order(
                symbol=validated_symbol,
                side=validated_side,
                order_type=validated_order_type,
                quantity=validated_quantity,
                price=validated_price
            )
            
            # Print order response
            self._print_order_response(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Order placement failed: {str(e)}")
            raise
    
    def _print_order_summary(self, symbol: str, side: str, order_type: str,
                            quantity: float, price: Optional[float]) -> None:
        """
        Print order request summary
        
        Args:
            symbol: Trading symbol
            side: Order side
            order_type: Order type
            quantity: Order quantity
            price: Order price (None for MARKET)
        """
        print("\n" + "="*60)
        print("ORDER REQUEST SUMMARY")
        print("="*60)
        print(f"Symbol:      {symbol}")
        print(f"Side:        {side}")
        print(f"Type:        {order_type}")
        print(f"Quantity:    {quantity}")
        if price:
            print(f"Price:       {price}")
        else:
            print(f"Price:       MARKET PRICE")
        print("="*60 + "\n")
        
        logger.info(f"Order Summary: {order_type} {side} {quantity} {symbol} @ {price if price else 'MARKET'}")
    
    def _print_order_response(self, response: Dict) -> None:
        """
        Print order response details
        
        Args:
            response: Order response from API
        """
        print("\n" + "="*60)
        print("ORDER RESPONSE")
        print("="*60)
        
        # Extract key fields
        order_id = response.get('orderId', 'N/A')
        client_order_id = response.get('clientOrderId', 'N/A')
        status = response.get('status', 'N/A')
        symbol = response.get('symbol', 'N/A')
        side = response.get('side', 'N/A')
        order_type = response.get('type', 'N/A')
        
        # Quantity info
        orig_qty = response.get('origQty', 'N/A')
        executed_qty = response.get('executedQty', '0')
        
        # Price info
        price = response.get('price', 'N/A')
        avg_price = response.get('avgPrice', '0')
        
        # Timestamps
        update_time = response.get('updateTime', 'N/A')
        
        print(f"Order ID:          {order_id}")
        print(f"Client Order ID:   {client_order_id}")
        print(f"Status:            {status}")
        print(f"Symbol:            {symbol}")
        print(f"Side:              {side}")
        print(f"Type:              {order_type}")
        print(f"Original Qty:      {orig_qty}")
        print(f"Executed Qty:      {executed_qty}")
        print(f"Price:             {price}")
        
        if avg_price and float(avg_price) > 0:
            print(f"Average Price:     {avg_price}")
        
        print(f"Update Time:       {update_time}")
        print("="*60)
        
        # Success/failure message
        if status == 'FILLED':
            print("✓ ORDER FILLED SUCCESSFULLY")
        elif status == 'NEW':
            print("✓ ORDER PLACED SUCCESSFULLY (PENDING)")
        elif status == 'PARTIALLY_FILLED':
            print("⚠ ORDER PARTIALLY FILLED")
        elif status == 'CANCELED':
            print("✗ ORDER CANCELED")
        elif status == 'REJECTED':
            print("✗ ORDER REJECTED")
        else:
            print(f"ℹ ORDER STATUS: {status}")
        
        print("="*60 + "\n")
        
        logger.info(f"Order Response: ID={order_id}, Status={status}, ExecutedQty={executed_qty}")
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """
        Get order status
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Order details dictionary
        """
        logger.info(f"Querying order status for Order ID: {order_id}")
        
        try:
            response = self.client.get_order(symbol, order_id)
            self._print_order_response(response)
            return response
        except Exception as e:
            logger.error(f"Failed to get order status: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an order
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
            
        Returns:
            Cancellation response dictionary
        """
        logger.info(f"Attempting to cancel Order ID: {order_id}")
        
        try:
            response = self.client.cancel_order(symbol, order_id)
            print(f"\n✓ Order {order_id} canceled successfully\n")
            return response
        except Exception as e:
            logger.error(f"Failed to cancel order: {str(e)}")
            print(f"\n✗ Failed to cancel order: {str(e)}\n")
            raise
