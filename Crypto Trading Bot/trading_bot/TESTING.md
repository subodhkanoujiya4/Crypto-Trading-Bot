# Testing Guide

This document provides comprehensive testing scenarios for the trading bot.

## Prerequisites

Before testing, ensure:
- ✅ Python 3.8+ installed
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Binance Futures Testnet account created
- ✅ API credentials configured
- ✅ Testnet funds available (get from faucet)

## Test 1: Connection Test

**Purpose**: Verify API credentials and connectivity

```bash
python cli.py --test-connection
```

**Expected Result**: 
- ✓ Connection successful
- ✓ Account access successful
- Shows wallet balance

**Possible Issues**:
- Invalid credentials: Check API key/secret
- Network error: Check internet connection
- Timeout: Try again or check testnet status

## Test 2: Market Order - BUY

**Purpose**: Test market buy order execution

```bash
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected Result**:
- Order request summary displayed
- Order status: FILLED
- Executed quantity: 0.001
- Average price shown
- Success message displayed

**Verification**:
1. Check log file in `logs/` directory
2. Login to testnet and verify position
3. Check order history in testnet UI

## Test 3: Market Order - SELL

**Purpose**: Test market sell order execution

```bash
python cli.py -s ETHUSDT -d SELL -t MARKET -q 0.01
```

**Expected Result**:
- Order executed immediately
- Status: FILLED
- Executed at current market price

## Test 4: Limit Order - BUY

**Purpose**: Test limit buy order placement

```bash
python cli.py -s BTCUSDT -d BUY -t LIMIT -q 0.001 -p 40000
```

**Expected Result**:
- Order status: NEW (pending)
- Order remains in order book
- Will fill when price reaches 40000

**Verification**:
- Check open orders in testnet UI
- Order should appear in order book

## Test 5: Limit Order - SELL

**Purpose**: Test limit sell order placement

```bash
python cli.py -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 5000
```

**Expected Result**:
- Order status: NEW
- Order posted to order book
- Waiting for price to reach 5000

## Test 6: Input Validation

**Purpose**: Test error handling for invalid inputs

### Test 6.1: Missing Price for LIMIT Order

```bash
python cli.py -s BTCUSDT -d BUY -t LIMIT -q 0.001
```

**Expected Result**: Error message about missing price

### Test 6.2: Invalid Quantity

```bash
python cli.py -s BTCUSDT -d BUY -t MARKET -q -0.001
```

**Expected Result**: Validation error for negative quantity

### Test 6.3: Invalid Symbol

```bash
python cli.py -s INVALID -d BUY -t MARKET -q 0.001
```

**Expected Result**: Symbol validation error or API error

### Test 6.4: Invalid Side

```bash
python cli.py -s BTCUSDT -d INVALID -d MARKET -q 0.001
```

**Expected Result**: Argument parser error (invalid choice)

## Test 7: Different Trading Pairs

**Purpose**: Test with various trading symbols

```bash
# BNB
python cli.py -s BNBUSDT -d BUY -t MARKET -q 0.1

# Solana
python cli.py -s SOLUSDT -d BUY -t MARKET -q 1

# Cardano
python cli.py -s ADAUSDT -d BUY -t MARKET -q 10

# XRP
python cli.py -s XRPUSDT -d BUY -t MARKET -q 10
```

**Expected Result**: All orders execute successfully

## Test 8: Logging Verification

**Purpose**: Verify comprehensive logging

**Steps**:
1. Execute any order
2. Check `logs/` directory
3. Open the most recent log file

**Expected Log Contents**:
- Session start timestamp
- API credentials loaded (not the actual keys!)
- Client initialization
- Parameter validation steps
- API request details (method, endpoint, parameters)
- API response (status code, full response body)
- Order summary and result

**Log File Checklist**:
- ✅ Timestamp on every line
- ✅ Log level (INFO, DEBUG, ERROR)
- ✅ Module name
- ✅ Clear, descriptive messages
- ✅ No sensitive data exposure (API secrets masked)
- ✅ Complete error stack traces (if errors occur)

## Test 9: Error Handling

**Purpose**: Test various error scenarios

### Test 9.1: Network Error Simulation

```bash
# Disconnect internet, then run:
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected Result**: Connection error with clear message

### Test 9.2: Invalid API Credentials

```bash
# Set invalid credentials
export BINANCE_API_KEY="invalid"
export BINANCE_API_SECRET="invalid"

python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected Result**: Authentication error

### Test 9.3: Insufficient Balance

```bash
# Try to place a very large order
python cli.py -s BTCUSDT -d BUY -t MARKET -q 100
```

**Expected Result**: Insufficient margin error

## Test 10: CLI Help and Version

**Purpose**: Test CLI documentation

```bash
# Help
python cli.py --help
python cli.py -h

# Version
python cli.py --version
```

**Expected Result**: 
- Help displays all options
- Examples shown
- Version displays correctly

## Test 11: Log Levels

**Purpose**: Test different logging verbosity

```bash
# Debug level (most verbose)
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001 --log-level DEBUG

# Info level (default)
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001 --log-level INFO

# Warning level (minimal)
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001 --log-level WARNING
```

**Expected Result**: 
- DEBUG: All debug messages in log
- INFO: Standard operational info
- WARNING: Only warnings and errors

## Test 12: Short vs Long Options

**Purpose**: Verify both option formats work

```bash
# Long options
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Short options
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected Result**: Both produce identical results

## Test 13: Case Insensitivity

**Purpose**: Test case-insensitive inputs

```bash
# Lowercase
python cli.py -s btcusdt -d buy -t market -q 0.001

# Mixed case
python cli.py -s BtcUsDt -d BuY -t MaRkEt -q 0.001
```

**Expected Result**: All converted to uppercase, orders execute

## Test 14: Concurrent Orders

**Purpose**: Test rapid order placement

```bash
# Run multiple orders in quick succession
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001 &
python cli.py -s ETHUSDT -d BUY -t MARKET -q 0.01 &
python cli.py -s BNBUSDT -d BUY -t MARKET -q 0.1 &
wait
```

**Expected Result**: All orders execute independently

## Test Results Template

Copy this template to track your testing:

```
Testing Date: __________
Tester: __________

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Connection Test | ☐ Pass ☐ Fail | |
| 2 | Market BUY | ☐ Pass ☐ Fail | |
| 3 | Market SELL | ☐ Pass ☐ Fail | |
| 4 | Limit BUY | ☐ Pass ☐ Fail | |
| 5 | Limit SELL | ☐ Pass ☐ Fail | |
| 6 | Input Validation | ☐ Pass ☐ Fail | |
| 7 | Different Pairs | ☐ Pass ☐ Fail | |
| 8 | Logging | ☐ Pass ☐ Fail | |
| 9 | Error Handling | ☐ Pass ☐ Fail | |
| 10 | CLI Help | ☐ Pass ☐ Fail | |
| 11 | Log Levels | ☐ Pass ☐ Fail | |
| 12 | Options Format | ☐ Pass ☐ Fail | |
| 13 | Case Sensitivity | ☐ Pass ☐ Fail | |
| 14 | Concurrent Orders | ☐ Pass ☐ Fail | |

Overall Result: ☐ All Pass ☐ Some Failures

Issues Found:
_____________________________________________
_____________________________________________
_____________________________________________
```

## Automated Testing

For automated testing, you can create a test script:

```python
# test_all.py
import subprocess
import sys

tests = [
    ('Connection Test', ['python', 'cli.py', '--test-connection']),
    ('Market BUY', ['python', 'cli.py', '-s', 'BTCUSDT', '-d', 'BUY', '-t', 'MARKET', '-q', '0.001']),
    ('Limit SELL', ['python', 'cli.py', '-s', 'ETHUSDT', '-d', 'SELL', '-t', 'LIMIT', '-q', '0.01', '-p', '5000']),
]

passed = 0
failed = 0

for name, cmd in tests:
    print(f"\nRunning: {name}")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"✓ {name} PASSED")
        passed += 1
    else:
        print(f"✗ {name} FAILED")
        failed += 1

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
print(f"{'='*50}")
```

## Performance Testing

Monitor performance metrics:

```bash
# Time a market order
time python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001

# Check log file sizes
ls -lh logs/

# Monitor memory usage (Linux)
/usr/bin/time -v python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

**Expected Performance**:
- Order execution: < 5 seconds
- Log file size: < 50 KB per order
- Memory usage: < 50 MB

## Best Practices for Testing

1. **Always test on testnet first**
2. **Keep test quantities small** (0.001 - 0.01)
3. **Verify in testnet UI** after each order
4. **Review log files** after each test
5. **Test error cases** thoroughly
6. **Document any issues** found
7. **Test with different network conditions**
8. **Clear test data** between test runs if needed

## Reporting Issues

If you find issues during testing:

1. Note the exact command used
2. Copy the error message
3. Include relevant log file excerpts
4. Note your environment (OS, Python version)
5. Describe expected vs actual behavior

---

**Last Updated**: January 30, 2024
