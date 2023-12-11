import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
print(f'ALPACA API KEY={os.getenv("ALPACA_API_KEY")}')
print(f'ALPACA SECRET KEY={os.getenv("ALPACA_SECRET_KEY")}')

# Fetching intraday data for the last 24 hours
now = datetime.now()
start = now - timedelta(days=1)
end = now
ticker = "AAPL"

# Interval for intraday data can be set to 1m, 5m, 15m, 30m, 60m, or 90m
data = yf.download(ticker, start=start, end=end, interval='15m')

# Since we're dealing with a much shorter time frame, adjust the windows
short_window = 5
long_window = 20
data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Generate signals
data['Signal'] = 0
data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
data['Position'] = data['Signal'].diff()

# Plotting
plt.figure(figsize=(10,5))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Short_MA'], label=f'Short {short_window}-Interval MA')
plt.plot(data['Long_MA'], label=f'Long {long_window}-Interval MA')
plt.plot(data[data['Position'] == 1].index, data['Short_MA'][data['Position'] == 1], '^', markersize=10, color='g', label='Buy Signal')
plt.plot(data[data['Position'] == -1].index, data['Short_MA'][data['Position'] == -1], 'v', markersize=10, color='r', label='Sell Signal')
plt.title(f'Intraday Moving Average Crossover Strategy for {ticker}')
plt.legend()
plt.show()
