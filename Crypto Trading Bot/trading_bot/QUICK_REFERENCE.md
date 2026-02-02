# Quick Reference Card

## Installation (30 seconds)

```bash
cd trading_bot
pip install -r requirements.txt
export BINANCE_API_KEY='your_key'
export BINANCE_API_SECRET='your_secret'
```

## Common Commands

### Test Connection
```bash
python cli.py --test-connection
```

### Market Buy Order
```bash
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

### Limit Sell Order
```bash
python cli.py -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3500
```

### Get Help
```bash
python cli.py --help
```

## File Structure Quick Map

```
bot/client.py       → Binance API communication
bot/orders.py       → Order placement logic
bot/validators.py   → Input validation
bot/logging_config.py → Logging setup
cli.py             → CLI entry point
logs/              → All log files
```

## Error Messages Decoder

| Error | Meaning | Solution |
|-------|---------|----------|
| API credentials not found | Env vars not set | Set BINANCE_API_KEY and BINANCE_API_SECRET |
| Validation Error | Bad input | Check symbol, quantity, price format |
| API Error -2015 | Invalid API key | Verify your API key |
| API Error -1022 | Invalid signature | Verify your API secret |
| API Error -2019 | Insufficient margin | Get testnet funds from faucet |
| Connection Error | Network issue | Check internet connection |

## CLI Options Cheat Sheet

| Short | Long | Required | Description | Example |
|-------|------|----------|-------------|---------|
| -s | --symbol | Yes | Trading pair | BTCUSDT |
| -d | --side | Yes | Buy or sell | BUY or SELL |
| -t | --type | Yes | Order type | MARKET or LIMIT |
| -q | --quantity | Yes | Amount | 0.001 |
| -p | --price | If LIMIT | Limit price | 45000 |
| | --log-level | No | Logging level | DEBUG, INFO |
| | --test-connection | No | Test API | (flag) |
| -h | --help | No | Show help | (flag) |

## Trading Symbols

Common Binance Futures symbols:
- BTCUSDT (Bitcoin)
- ETHUSDT (Ethereum)
- BNBUSDT (BNB)
- ADAUSDT (Cardano)
- SOLUSDT (Solana)
- XRPUSDT (XRP)
- DOGEUSDT (Dogecoin)

## Log File Locations

Logs are saved in: `logs/trading_bot_YYYYMMDD_HHMMSS.log`

View latest log:
```bash
ls -lt logs/ | head -2
cat logs/trading_bot_*.log | tail -50
```

## Typical Workflow

1. Set environment variables (once per session)
2. Test connection: `python cli.py --test-connection`
3. Place orders: `python cli.py -s SYMBOL -d SIDE -t TYPE -q QTY [-p PRICE]`
4. Check logs: `cat logs/trading_bot_*.log`
5. Verify on testnet UI: https://testnet.binancefuture.com/

## Getting Testnet Credentials

1. Go to: https://testnet.binancefuture.com/
2. Register/Login
3. Go to API Management
4. Create API Key
5. Copy API Key and Secret Key
6. Get testnet funds from faucet

## Documentation Files

- **README.md** - Main documentation
- **SETUP_GUIDE.md** - Detailed setup
- **TESTING.md** - Testing scenarios
- **ARCHITECTURE.md** - Code structure
- **SUBMISSION.md** - Submission checklist
- **QUICK_REFERENCE.md** - This file

## One-Liner Examples

```bash
# Market orders
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
python cli.py -s ETHUSDT -d SELL -t MARKET -q 0.01

# Limit orders
python cli.py -s BTCUSDT -d BUY -t LIMIT -q 0.001 -p 40000
python cli.py -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 5000

# Different pairs
python cli.py -s BNBUSDT -d BUY -t MARKET -q 0.1
python cli.py -s SOLUSDT -d BUY -t MARKET -q 1
python cli.py -s ADAUSDT -d BUY -t MARKET -q 10

# With debug logging
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001 --log-level DEBUG
```

## Exit Codes

- **0** - Success
- **1** - Error (validation, API, network)
- **130** - User cancelled (Ctrl+C)

## Environment Variables

```bash
# Required
BINANCE_API_KEY       - Your Binance testnet API key
BINANCE_API_SECRET    - Your Binance testnet secret key

# Optional (defaults shown)
LOG_LEVEL=INFO        - Logging verbosity
```

## Troubleshooting Quick Fixes

### Can't connect?
```bash
curl https://testnet.binancefuture.com/fapi/v1/ping
```

### Module not found?
```bash
pip install -r requirements.txt --upgrade
```

### Permission denied?
```bash
chmod +x cli.py
```

### Environment vars not working?
```bash
# Check if set
echo $BINANCE_API_KEY
echo $BINANCE_API_SECRET

# Re-export if empty
export BINANCE_API_KEY='your_key'
export BINANCE_API_SECRET='your_secret'
```

## Performance Expectations

- Order placement: < 5 seconds
- API response: < 2 seconds
- Memory usage: < 50 MB
- Log file: < 50 KB per order

## Best Practices

1. Always test on testnet first
2. Use small quantities for testing
3. Check logs after each order
4. Verify orders in testnet UI
5. Keep API keys secure
6. Review validation errors carefully

## Links

- Testnet: https://testnet.binancefuture.com/
- API Docs: https://binance-docs.github.io/apidocs/futures/en/
- This repo: [Your GitHub URL]

---

**Print this card for quick reference while using the bot!**
