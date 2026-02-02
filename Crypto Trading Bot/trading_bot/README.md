# Binance Futures Trading Bot

A Python-based trading bot for placing orders on Binance Futures Testnet (USDT-M). This bot provides a clean, modular structure with comprehensive logging and error handling.

## Features

✅ **Order Types**: Market and Limit orders  
✅ **Both Sides**: BUY and SELL  
✅ **CLI Interface**: Easy-to-use command-line interface with argparse  
✅ **Input Validation**: Comprehensive parameter validation  
✅ **Error Handling**: Robust exception handling for API, network, and validation errors  
✅ **Logging**: Detailed logging of all requests, responses, and errors  
✅ **Modular Structure**: Clean separation of concerns (client, orders, validators, CLI)  
✅ **Type Hints**: Full type annotations for better code quality  

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Binance API client wrapper
│   ├── orders.py             # Order placement and management logic
│   ├── validators.py         # Input validation
│   └── logging_config.py     # Logging configuration
├── cli.py                    # CLI entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── logs/                     # Log files (created automatically)
```

## Setup

### 1. Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- API credentials from Binance Futures Testnet

### 2. Get Binance Testnet Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Register/login with your email
3. Navigate to API Management
4. Create new API key and save both:
   - API Key
   - API Secret

### 3. Install Dependencies

```bash
# Clone or download the repository
cd trading_bot

# Install required packages
pip install -r requirements.txt
```

### 4. Configure API Credentials

Set your API credentials as environment variables:

**Linux/Mac:**
```bash
export BINANCE_API_KEY='your_api_key_here'
export BINANCE_API_SECRET='your_api_secret_here'
```

**Windows (Command Prompt):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY='your_api_key_here'
$env:BINANCE_API_SECRET='your_api_secret_here'
```

### 5. Test Connection

```bash
python cli.py --test-connection
```

## Usage

### Basic Command Structure

```bash
python cli.py --symbol SYMBOL --side SIDE --type TYPE --quantity QUANTITY [--price PRICE]
```

### Required Arguments

- `--symbol` or `-s`: Trading symbol (e.g., BTCUSDT, ETHUSDT)
- `--side` or `-d`: Order side (BUY or SELL)
- `--type` or `-t`: Order type (MARKET or LIMIT)
- `--quantity` or `-q`: Order quantity

### Optional Arguments

- `--price` or `-p`: Order price (required for LIMIT orders)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR) - default: INFO
- `--test-connection`: Test API connection and exit
- `--version`: Show version and exit
- `--help` or `-h`: Show help message

## Examples

### 1. Market Buy Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Or using short options:
```bash
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected Output:**
```
📝 Logging to: logs/trading_bot_20240130_143022.log

============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:      BTCUSDT
Side:        BUY
Type:        MARKET
Quantity:    0.001
Price:       MARKET PRICE
============================================================

============================================================
ORDER RESPONSE
============================================================
Order ID:          12345678
Client Order ID:   web_abc123def456
Status:            FILLED
Symbol:            BTCUSDT
Side:              BUY
Type:              MARKET
Original Qty:      0.001
Executed Qty:      0.001
Price:             0
Average Price:     45000.50
Update Time:       1706623822000
============================================================
✓ ORDER FILLED SUCCESSFULLY
============================================================
```

### 2. Limit Sell Order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500.00
```

Or using short options:
```bash
python cli.py -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3500.00
```

**Expected Output:**
```
📝 Logging to: logs/trading_bot_20240130_143525.log

============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:      ETHUSDT
Side:        SELL
Type:        LIMIT
Quantity:    0.01
Price:       3500.0
============================================================

============================================================
ORDER RESPONSE
============================================================
Order ID:          12345679
Client Order ID:   web_xyz789abc012
Status:            NEW
Symbol:            ETHUSDT
Side:              SELL
Type:              LIMIT
Original Qty:      0.01
Executed Qty:      0
Price:             3500.0
Update Time:       1706624125000
============================================================
✓ ORDER PLACED SUCCESSFULLY (PENDING)
============================================================
```

### 3. More Examples

**BNB Market Sell:**
```bash
python cli.py -s BNBUSDT -d SELL -t MARKET -q 0.1
```

**SOL Limit Buy:**
```bash
python cli.py -s SOLUSDT -d BUY -t LIMIT -q 1 -p 100.50
```

**With Debug Logging:**
```bash
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001 --log-level DEBUG
```

## Logging

All operations are logged to files in the `logs/` directory with timestamps:
- Format: `trading_bot_YYYYMMDD_HHMMSS.log`
- Includes: API requests, responses, errors, validation steps
- Console: Shows only warnings and errors
- Log file: Contains all DEBUG level information

### Log File Contents

Each log file contains:
- Session start information
- API connection details
- Order validation steps
- Complete API request parameters
- Full API response data
- All errors and exceptions with stack traces

## Error Handling

The bot handles various error scenarios:

### Validation Errors
```bash
# Missing price for LIMIT order
python cli.py -s BTCUSDT -d BUY -t LIMIT -q 0.001

✗ Error: Price (--price) is required for LIMIT orders
```

### Invalid Input
```bash
# Invalid quantity
python cli.py -s BTCUSDT -d BUY -t MARKET -q -0.001

✗ Validation Error: Quantity must be positive, got: -0.001
```

### API Errors
```bash
# Insufficient balance
✗ Unexpected Error: API Error [-2019]: Margin is insufficient.
```

### Network Errors
- Connection timeouts (10 second timeout)
- Connection failures
- DNS resolution issues

## Code Quality Features

- ✅ **Type Hints**: Full type annotations throughout
- ✅ **Docstrings**: Comprehensive documentation for all functions/classes
- ✅ **Logging**: Structured logging at appropriate levels
- ✅ **Error Handling**: Try-except blocks with specific exception handling
- ✅ **Input Validation**: Comprehensive parameter validation before API calls
- ✅ **Separation of Concerns**: Client, orders, validation, and CLI are separate modules
- ✅ **DRY Principle**: Reusable components and minimal code duplication

## Assumptions

1. **Testnet Environment**: The bot is configured for Binance Futures Testnet by default
2. **USDT-M Futures**: Uses USDT-margined futures (not Coin-margined)
3. **Time in Force**: LIMIT orders use GTC (Good Till Cancel) by default
4. **Authentication**: Expects credentials via environment variables for security
5. **Network**: Assumes stable internet connection
6. **Precision**: Does not adjust order quantities/prices to match exchange filters (relies on API validation)

## Troubleshooting

### "API credentials not found"
- Ensure environment variables are set correctly
- Check for typos in variable names
- In new terminal windows, you may need to export variables again

### "Connection Error"
- Check internet connection
- Verify testnet URL is accessible: https://testnet.binancefuture.com
- Check firewall settings

### "Invalid symbol" or "Unknown symbol"
- Verify symbol exists on Binance Futures Testnet
- Common symbols: BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT
- Symbol must be uppercase

### "Insufficient margin"
- Your testnet account needs sufficient balance
- Get testnet USDT from the testnet faucet

## API Documentation

- [Binance Futures API](https://binance-docs.github.io/apidocs/futures/en/)
- [Binance Futures Testnet](https://testnet.binancefuture.com/)

## License

This project is for educational purposes as part of a job application assignment.

## Contact

For questions or issues, please contact the development team.

---

**Note**: This bot is designed for Binance Futures Testnet only. Do not use with real trading credentials or on production environments without proper modifications and testing.
