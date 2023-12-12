import alpaca_trade_api as tradeapi
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Alpaca API credentials
API_KEY = os.getenv('TRADER_KEY')
API_SECRET = os.getenv('TRADER_SECRET')
BASE_URL = os.getenv('TRADER_ENDPOINT')



# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v1')

# Function to check if the market is open
def is_market_open():
    clock = api.get_clock()
    return clock.is_open

# Swing trading strategy
def swing_trading_strategy(symbol, short_window, long_window):
    if not is_market_open():
        print("Market is closed. Skipping trade execution.")
        return

    # Get historical data
    historical_data = api.get_barset(
        symbols=symbol,
        timeframe='day',
        limit=long_window + 1
    )[symbol]

    if len(historical_data) < long_window + 1:
        print(f"Not enough historical data available for {symbol}. Skipping trade execution.")
        return

    # Calculate moving averages
    short_ma = sum(bar.close for bar in historical_data[-short_window:]) / short_window
    long_ma = sum(bar.close for bar in historical_data[-long_window:]) / long_window

    # Check for buy/sell signals
    if short_ma > long_ma:
        # Buy signal
        print(f"Buy signal for {symbol}")
        try:
            # Place a market order to buy 1 share of the symbol
            api.submit_order(
                symbol=symbol,
                qty=10,
                side='buy',
                type='market',
                time_in_force='gtc'  # Good Till Cancelled
            )
            print("Buy order placed successfully.")
        except Exception as e:
            print(f"Error placing buy order: {e}")
    elif short_ma < long_ma:
        # Sell signal
        print(f"Sell signal for {symbol}")
        try:
            # Place a market order to sell 1 share of the symbol
            api.submit_order(
                symbol=symbol,
                qty=10,
                side='sell',
                type='market',
                time_in_force='gtc'  # Good Till Cancelled
            )
            print("Sell order placed successfully.")
        except Exception as e:
            print(f"Error placing sell order: {e}")

# Main loop
while True:
    try:
        # Define your swing trading parameters
        symbol = 'WBD'  # The stock you want to swing trade
        short_window = 10  # Short-term moving average window
        long_window = 30  # Long-term moving average window

        # Execute the swing trading strategy
        swing_trading_strategy(symbol, short_window, long_window)

        # Sleep for a period (e.g., 1 day) before checking again
        time.sleep(86400)  # Sleep for 24 hours
    except KeyboardInterrupt:
        print("Exiting the swing trading bot.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(3600)  # Wait 1 hour before retrying
