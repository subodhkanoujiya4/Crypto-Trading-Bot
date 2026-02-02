"""
Input Validation Module
Validates trading parameters before order placement
"""

import re
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class OrderValidator:
    """
    Validator for order parameters
    """
    
    VALID_SIDES = ['BUY', 'SELL']
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT']
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol format
        
        Args:
            symbol: Trading symbol (e.g., BTCUSDT)
            
        Returns:
            Uppercase symbol
            
        Raises:
            ValidationError: If symbol format is invalid
        """
        if not symbol:
            raise ValidationError("Symbol cannot be empty")
        
        # Convert to uppercase
        symbol = symbol.upper()
        
        # Basic format check (alphanumeric)
        if not re.match(r'^[A-Z0-9]+$', symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        # Most Binance symbols end with USDT, BUSD, or BTC
        if len(symbol) < 6:
            raise ValidationError(f"Symbol too short: {symbol}")
        
        logger.debug(f"Symbol validated: {symbol}")
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """
        Validate order side
        
        Args:
            side: Order side (BUY or SELL)
            
        Returns:
            Uppercase side
            
        Raises:
            ValidationError: If side is invalid
        """
        if not side:
            raise ValidationError("Side cannot be empty")
        
        side = side.upper()
        
        if side not in OrderValidator.VALID_SIDES:
            raise ValidationError(f"Invalid side: {side}. Must be one of {OrderValidator.VALID_SIDES}")
        
        logger.debug(f"Side validated: {side}")
        return side
    
    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """
        Validate order type
        
        Args:
            order_type: Order type (MARKET or LIMIT)
            
        Returns:
            Uppercase order type
            
        Raises:
            ValidationError: If order type is invalid
        """
        if not order_type:
            raise ValidationError("Order type cannot be empty")
        
        order_type = order_type.upper()
        
        if order_type not in OrderValidator.VALID_ORDER_TYPES:
            raise ValidationError(
                f"Invalid order type: {order_type}. Must be one of {OrderValidator.VALID_ORDER_TYPES}"
            )
        
        logger.debug(f"Order type validated: {order_type}")
        return order_type
    
    @staticmethod
    def validate_quantity(quantity: str, symbol: str = "") -> float:
        """
        Validate order quantity
        
        Args:
            quantity: Order quantity as string
            symbol: Trading symbol (for context in error messages)
            
        Returns:
            Quantity as float
            
        Raises:
            ValidationError: If quantity is invalid
        """
        try:
            qty = float(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid quantity format: {quantity}")
        
        if qty <= 0:
            raise ValidationError(f"Quantity must be positive, got: {qty}")
        
        # Check for reasonable upper bound (prevent accidental large orders)
        if qty > 1000000:
            raise ValidationError(
                f"Quantity seems too large: {qty}. Please verify this is correct."
            )
        
        logger.debug(f"Quantity validated: {qty}")
        return qty
    
    @staticmethod
    def validate_price(price: str, order_type: str, symbol: str = "") -> Optional[float]:
        """
        Validate order price
        
        Args:
            price: Order price as string
            order_type: Order type (MARKET or LIMIT)
            symbol: Trading symbol (for context in error messages)
            
        Returns:
            Price as float, or None for MARKET orders
            
        Raises:
            ValidationError: If price is invalid
        """
        # MARKET orders don't need price
        if order_type == 'MARKET':
            if price:
                logger.warning(f"Price provided for MARKET order will be ignored: {price}")
            return None
        
        # LIMIT orders require price
        if order_type == 'LIMIT':
            if not price:
                raise ValidationError("Price is required for LIMIT orders")
            
            try:
                price_float = float(price)
            except (ValueError, TypeError):
                raise ValidationError(f"Invalid price format: {price}")
            
            if price_float <= 0:
                raise ValidationError(f"Price must be positive, got: {price_float}")
            
            logger.debug(f"Price validated: {price_float}")
            return price_float
        
        return None
    
    @classmethod
    def validate_order_params(cls, symbol: str, side: str, order_type: str,
                             quantity: str, price: Optional[str] = None) -> Tuple[str, str, str, float, Optional[float]]:
        """
        Validate all order parameters at once
        
        Args:
            symbol: Trading symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (optional)
            
        Returns:
            Tuple of validated parameters (symbol, side, order_type, quantity, price)
            
        Raises:
            ValidationError: If any parameter is invalid
        """
        logger.info("Validating order parameters...")
        
        try:
            validated_symbol = cls.validate_symbol(symbol)
            validated_side = cls.validate_side(side)
            validated_order_type = cls.validate_order_type(order_type)
            validated_quantity = cls.validate_quantity(quantity, validated_symbol)
            validated_price = cls.validate_price(price, validated_order_type, validated_symbol)
            
            logger.info("All parameters validated successfully")
            
            return (
                validated_symbol,
                validated_side,
                validated_order_type,
                validated_quantity,
                validated_price
            )
            
        except ValidationError as e:
            logger.error(f"Validation failed: {str(e)}")
            raise
