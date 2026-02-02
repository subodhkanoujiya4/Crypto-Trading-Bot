#!/usr/bin/env python3
"""
Demo Script for Trading Bot
Generates example orders and log files for demonstration purposes
"""

import os
import sys

# Example credentials (replace with your actual testnet credentials)
DEMO_API_KEY = "your_testnet_api_key"
DEMO_API_SECRET = "your_testnet_api_secret"


def run_demo():
    """Run demo orders"""
    
    print("="*70)
    print("TRADING BOT DEMO")
    print("="*70)
    print()
    print("This script will demonstrate the bot with example orders.")
    print()
    print("⚠️  IMPORTANT: This requires valid Binance Futures Testnet credentials!")
    print()
    
    # Check if credentials are set
    api_key = os.getenv('BINANCE_API_KEY', DEMO_API_KEY)
    api_secret = os.getenv('BINANCE_API_SECRET', DEMO_API_SECRET)
    
    if api_key == "your_testnet_api_key" or api_secret == "your_testnet_api_secret":
        print("❌ Please set your Binance Futures Testnet credentials:")
        print()
        print("   export BINANCE_API_KEY='your_actual_api_key'")
        print("   export BINANCE_API_SECRET='your_actual_api_secret'")
        print()
        print("   Or edit the DEMO_API_KEY and DEMO_API_SECRET in demo.py")
        print()
        return
    
    # Set environment variables for the demo
    os.environ['BINANCE_API_KEY'] = api_key
    os.environ['BINANCE_API_SECRET'] = api_secret
    
    demos = [
        {
            'name': 'Test Connection',
            'cmd': 'python cli.py --test-connection',
            'description': 'Testing API connectivity'
        },
        {
            'name': 'Market Buy Order (BTCUSDT)',
            'cmd': 'python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001',
            'description': 'Placing a small market buy order for Bitcoin'
        },
        {
            'name': 'Limit Sell Order (ETHUSDT)',
            'cmd': 'python cli.py -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 5000',
            'description': 'Placing a limit sell order for Ethereum at $5000'
        },
        {
            'name': 'Market Sell Order (BNBUSDT)',
            'cmd': 'python cli.py -s BNBUSDT -d SELL -t MARKET -q 0.1',
            'description': 'Placing a market sell order for BNB'
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{'='*70}")
        print(f"Demo {i}/{len(demos)}: {demo['name']}")
        print(f"{'='*70}")
        print(f"Description: {demo['description']}")
        print(f"Command: {demo['cmd']}")
        print()
        
        input("Press Enter to continue (or Ctrl+C to exit)...")
        
        # Run the command
        os.system(demo['cmd'])
        
        print()
    
    print("\n" + "="*70)
    print("DEMO COMPLETED")
    print("="*70)
    print()
    print("✅ Check the 'logs/' directory for detailed log files")
    print("✅ Each order generated a separate log file with full details")
    print()


if __name__ == '__main__':
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo cancelled by user\n")
        sys.exit(0)
