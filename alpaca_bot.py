import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import os
from dotenv import load_dotenv
import requests
import time

# Load environment variables
load_dotenv()

# Alpaca API credentials
API_KEY = os.getenv('ALPACA_API_KEY')
API_SECRET = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading URL
account_id = os.getenv('ACCOUNT_ID')
url = "https://broker-api.sandbox.alpaca.markets/"
modifier = f"v1/trading/accounts/{account_id}/orders"
AUTH_TOKEN = os.getenv('AUTH')

headers = {
    "accept": "application/json",
    "authorization": f"Basic {AUTH_TOKEN}"
}
# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v1')

# Function to check if the market is open
def is_market_open(api):
    try:
        clock = api.get_clock()
        return clock.is_open
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False

# Get historical data from Yahoo Finance
def get_historical_data(symbol):
    ticker_symbol = symbol.upper()
    now = datetime.now()
    start_date = now - timedelta(days=100)  # Adjust as needed

    try:
        data = yf.download(ticker_symbol, start=start_date, end=now)
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Calculate moving averages
def calculate_moving_averages(data, short_window, long_window):
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

# Implement the strategy
def moving_average_strategy(symbol, short_window, long_window):
    if not is_market_open(api):  # Check if market is open
        print("Market is not open. Skipping trade execution.")
        return
    data = get_historical_data(symbol)
    if data is None:
        return

    df = calculate_moving_averages(data, short_window, long_window)
    latest_data = df.iloc[-1]  # Get the latest data point

    # Check for buy/sell signals
    if latest_data['Short_MA'] > latest_data['Long_MA']:  
        # Buy signal
        print(f"Buy signal for {symbol}")
        response = requests.post(url + modifier, headers=headers, json=
            {
            "symbol": f"{symbol}",
            "qty": 1,
            "side": "buy",
            "type": "market",
            "time_in_force": "day"
            })
        print(response.text)
    elif latest_data['Short_MA'] < latest_data['Long_MA']:  
        # Sell signal
        print(f"Sell signal for {symbol}")
        response = requests.post(url + modifier, headers=headers, json=
            {
            "symbol": f"{symbol}",
            "qty": 1,
            "side": "sell",
            "type": "market",
            "time_in_force": "day"
            })
        print(response.text)

# Main loop
while True:
    try:
        # Run the strategy
        moving_average_strategy('AAPL', short_window=40, long_window=100)
        time.sleep(60)  # Wait for 1 minute
    except KeyboardInterrupt:
        print("Exiting the trading bot.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(300)  # Wait before retrying