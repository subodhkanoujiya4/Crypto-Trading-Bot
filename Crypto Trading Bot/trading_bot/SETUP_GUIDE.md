# Complete Setup Guide

This guide will walk you through setting up the trading bot from scratch.

## Step 1: Install Python

### Check Python Version
```bash
python --version
# or
python3 --version
```

You need Python 3.8 or higher. If you don't have it:

- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

## Step 2: Get Binance Futures Testnet Credentials

### 2.1 Create Testnet Account

1. Visit: https://testnet.binancefuture.com/
2. Click "Register" or login if you already have an account
3. Complete registration with your email

### 2.2 Generate API Keys

1. After login, go to your profile (top right)
2. Click "API Management" or "API Key"
3. Click "Generate API Key" or "Create API"
4. Save both values securely:
   - **API Key**: Long string starting with letters/numbers
   - **Secret Key**: Another long string (shown only once!)

⚠️ **IMPORTANT**: Copy your Secret Key immediately! It's only shown once.

### 2.3 Get Testnet Funds

1. In the testnet dashboard, look for "Faucet" or "Get Test Funds"
2. Click to receive test USDT (usually 10,000 USDT)
3. Funds appear instantly in your Futures wallet

## Step 3: Download the Trading Bot

### Option A: Clone from GitHub (if available)
```bash
git clone <repository_url>
cd trading_bot
```

### Option B: Extract from ZIP
```bash
unzip trading_bot.zip
cd trading_bot
```

## Step 4: Install Dependencies

```bash
# Make sure you're in the trading_bot directory
cd trading_bot

# Install required packages
pip install -r requirements.txt

# Or with pip3
pip3 install -r requirements.txt
```

**Expected output:**
```
Collecting requests>=2.31.0
  Downloading requests-2.31.0-py3-none-any.whl
Installing collected packages: requests
Successfully installed requests-2.31.0
```

## Step 5: Configure API Credentials

### Method 1: Environment Variables (Recommended)

**Linux/Mac:**
```bash
export BINANCE_API_KEY='your_actual_api_key_here'
export BINANCE_API_SECRET='your_actual_secret_key_here'
```

**Windows (Command Prompt):**
```cmd
set BINANCE_API_KEY=your_actual_api_key_here
set BINANCE_API_SECRET=your_actual_secret_key_here
```

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY='your_actual_api_key_here'
$env:BINANCE_API_SECRET='your_actual_secret_key_here'
```

### Method 2: .env File (Alternative)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your favorite text editor:
   ```bash
   nano .env
   # or
   vim .env
   # or
   code .env  # VS Code
   ```

3. Replace the placeholder values:
   ```
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_secret_key_here
   ```

4. Load the environment (if using .env file):
   ```bash
   # Linux/Mac
   source .env
   
   # Windows - you'll need to set variables manually from the file
   ```

## Step 6: Test the Connection

```bash
python cli.py --test-connection
```

**Expected successful output:**
```
📝 Logging to: logs/trading_bot_20240130_143022.log

Testing connection to Binance Futures Testnet...
✓ Connection successful!
✓ Account access successful!
  Total Wallet Balance: 10000.00 USDT
```

**If you see errors:**

❌ **"API credentials not found"**
- Your environment variables aren't set correctly
- Check spelling: `BINANCE_API_KEY` and `BINANCE_API_SECRET`
- Try setting them again in your current terminal

❌ **"Connection failed" or "Network error"**
- Check your internet connection
- Try visiting https://testnet.binancefuture.com/ in your browser
- Check firewall settings

❌ **"API Error -2015: Invalid API key"**
- Your API key is incorrect
- Copy it again from Binance testnet
- Make sure there are no extra spaces

❌ **"API Error -1022: Signature verification failed"**
- Your API secret is incorrect
- Make sure you copied the full secret key
- Regenerate keys if needed

## Step 7: Place Your First Order

### Test with a Market Order

```bash
python cli.py -s BTCUSDT -d BUY -t MARKET -q 0.001
```

This will:
- Buy 0.001 BTC
- At current market price
- Using USDT from your testnet balance

**Expected output:**
```
📝 Logging to: logs/trading_bot_20240130_143525.log

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
Status:            FILLED
Symbol:            BTCUSDT
Side:              BUY
...
✓ ORDER FILLED SUCCESSFULLY
============================================================
```

### Test with a Limit Order

```bash
python cli.py -s ETHUSDT -d SELL -t LIMIT -q 0.01 -p 3500
```

This will:
- Place a sell order for 0.01 ETH
- At a limit price of $3500
- Order stays open until filled or cancelled

## Step 8: View Logs

```bash
# List log files
ls logs/

# View the most recent log
cat logs/trading_bot_*.log | tail -50

# Or use your favorite text editor
nano logs/trading_bot_20240130_143022.log
```

## Common Issues and Solutions

### Issue: "command not found: python"
**Solution**: Try `python3` instead of `python`

### Issue: "No module named 'requests'"
**Solution**: 
```bash
pip install requests
# or
pip3 install requests
```

### Issue: "Permission denied"
**Solution**: 
```bash
# Linux/Mac - make script executable
chmod +x cli.py
```

### Issue: Environment variables lost after closing terminal
**Solution**: Add to your shell profile (~/.bashrc, ~/.zshrc, etc.):
```bash
echo 'export BINANCE_API_KEY="your_key"' >> ~/.bashrc
echo 'export BINANCE_API_SECRET="your_secret"' >> ~/.bashrc
source ~/.bashrc
```

## Next Steps

1. ✅ Read the main [README.md](README.md) for more examples
2. ✅ Try different trading symbols (BNBUSDT, ADAUSDT, SOLUSDT)
3. ✅ Experiment with different order sizes
4. ✅ Check the Binance testnet UI to see your orders
5. ✅ Review log files to understand the API communication

## Need Help?

- Check the [README.md](README.md) for usage examples
- Review log files for detailed error messages
- Verify your credentials at https://testnet.binancefuture.com/
- Make sure you have testnet USDT balance

## Security Reminders

⚠️ **Never commit real credentials to GitHub**
⚠️ **Use testnet only for this project**
⚠️ **Don't share your API keys publicly**
⚠️ **Testnet funds have no real value**

---

Congratulations! You're ready to use the trading bot. 🎉
