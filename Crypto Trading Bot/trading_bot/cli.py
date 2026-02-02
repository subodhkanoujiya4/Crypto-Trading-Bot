#!/usr/bin/env python3
"""
Trading Bot CLI
Command-line interface for placing orders on Binance Futures Testnet
"""

import argparse
import sys
import os
import requests
from pathlib import Path
from typing import Optional

from bot import BinanceClient, OrderManager, ValidationError, setup_logging, get_logger

# Get logger for this module
logger = None  # Will be initialized after logging setup


def load_credentials() -> tuple[str, str]:
    """
    Load API credentials from environment variables
    
    Returns:
        Tuple of (api_key, api_secret)
        
    Raises:
        EnvironmentError: If credentials are not found
    """
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        raise EnvironmentError(
            "API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.\n"
            "Example:\n"
            "  export BINANCE_API_KEY='your_api_key'\n"
            "  export BINANCE_API_SECRET='your_api_secret'"
        )
    
    return api_key, api_secret


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Trading Bot for Binance Futures Testnet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Place a limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500

  # Use short options
  python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001

Environment Variables:
  BINANCE_API_KEY     Your Binance API key
  BINANCE_API_SECRET  Your Binance API secret
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-s', '--symbol',
        type=str,
        required=True,
        help='Trading symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        '-d', '--side',
        type=str,
        required=True,
        choices=['BUY', 'SELL', 'buy', 'sell'],
        help='Order side: BUY or SELL'
    )
    
    parser.add_argument(
        '-t', '--type',
        type=str,
        required=True,
        choices=['MARKET', 'LIMIT', 'market', 'limit'],
        help='Order type: MARKET or LIMIT'
    )
    
    parser.add_argument(
        '-q', '--quantity',
        type=str,
        required=True,
        help='Order quantity (e.g., 0.001)'
    )
    
    # Optional arguments
    parser.add_argument(
        '-p', '--price',
        type=str,
        default=None,
        help='Order price (required for LIMIT orders)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='Test API connection and exit'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Trading Bot v1.0.0'
    )
    
    return parser


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments
    
    Args:
        args: Parsed arguments
        
    Raises:
        ValueError: If arguments are invalid
    """
    # Check if price is provided for LIMIT orders
    if args.type.upper() == 'LIMIT' and not args.price:
        raise ValueError("Price (--price) is required for LIMIT orders")
    
    # Warn if price is provided for MARKET orders
    if args.type.upper() == 'MARKET' and args.price:
        print("⚠ Warning: Price will be ignored for MARKET orders")


def test_connection(client: BinanceClient) -> bool:
    """
    Test connection to Binance API
    
    Args:
        client: BinanceClient instance
        
    Returns:
        True if connection successful
    """
    print("\nTesting connection to Binance Futures Testnet...")
    
    if client.test_connectivity():
        print("✓ Connection successful!")
        
        # Try to get account info
        try:
            account = client.get_account_info()
            print(f"✓ Account access successful!")
            print(f"  Total Wallet Balance: {account.get('totalWalletBalance', 'N/A')} USDT")
            return True
        except Exception as e:
            print(f"✗ Failed to access account: {str(e)}")
            return False
    else:
        print("✗ Connection failed!")
        return False


def main():
    """
    Main entry point for CLI
    """
    global logger
    
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    log_file = setup_logging(log_level=args.log_level)
    logger = get_logger(__name__)
    
    print(f"\n📝 Logging to: {log_file}\n")
    
    try:
        # Load credentials
        logger.info("Loading API credentials...")
        api_key, api_secret = load_credentials()
        
        # Initialize client
        logger.info("Initializing Binance client...")
        client = BinanceClient(api_key, api_secret, testnet=True)
        
        # Test connection if requested
        if args.test_connection:
            success = test_connection(client)
            sys.exit(0 if success else 1)
        
        # Validate arguments
        validate_args(args)
        
        # Initialize order manager
        order_manager = OrderManager(client)
        
        # Place order
        logger.info("Placing order...")
        response = order_manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        # Success
        logger.info("Order completed successfully")
        sys.exit(0)
        
    except EnvironmentError as e:
        print(f"\n✗ Configuration Error: {str(e)}\n")
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
        
    except ValidationError as e:
        print(f"\n✗ Validation Error: {str(e)}\n")
        logger.error(f"Validation error: {str(e)}")
        sys.exit(1)
        
    except ValueError as e:
        print(f"\n✗ Error: {str(e)}\n")
        logger.error(f"Value error: {str(e)}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user\n")
        logger.warning("Operation cancelled by user")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n✗ Unexpected Error: {str(e)}\n")
        logger.exception("Unexpected error occurred")
        sys.exit(1)


if __name__ == '__main__':
    main()
