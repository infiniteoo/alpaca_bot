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
# Define maximum position size
max_position_size = 1000  # Set your maximum position size in dollars

# Momentum trading strategy
def momentum_trading_strategy(symbol, threshold_percentage):
    if not is_market_open():
        print("Market is closed. Skipping trade execution.")
        return

    # Get current price
    current_price = api.get_latest_trade(symbol).price

    # Define buy/sell thresholds
    buy_threshold = current_price * (1 + threshold_percentage)
    sell_threshold = current_price * (1 - threshold_percentage)

    # Check for buy/sell signals
    if current_price > buy_threshold:
        # Buy signal
        print(f"Buy signal for {symbol}")
        try:
            # Calculate the number of shares to buy based on the maximum position size
            max_buy_qty = max_position_size // current_price

            # Place a market order to buy up to max_buy_qty shares of the symbol
            api.submit_order(
                symbol=symbol,
                qty=max_buy_qty,
                side='buy',
                type='market',
                time_in_force='gtc'  # Good Till Cancelled
            )
            print(f"Buy order placed for {max_buy_qty} shares.")
        except Exception as e:
            print(f"Error placing buy order: {e}")
    elif current_price < sell_threshold:
        # Sell signal
        print(f"Sell signal for {symbol}")
        try:
            # Check your existing position for the symbol
            existing_position = api.get_position(symbol)

            if existing_position is not None:
                # Calculate the number of shares to sell (up to the current position size)
                sell_qty = min(existing_position.qty, max_buy_qty)

                # Place a market order to sell the calculated quantity of shares
                api.submit_order(
                    symbol=symbol,
                    qty=sell_qty,
                    side='sell',
                    type='market',
                    time_in_force='gtc'  # Good Till Cancelled
                )
                print(f"Sell order placed for {sell_qty} shares.")
            else:
                print(f"You don't own any shares of {symbol}. Skipping sell order.")
        except Exception as e:
            print(f"Error placing sell order: {e}")

# Main loop
while True:
    try:
        # Define your momentum trading parameters
        symbol = 'AMD'  # The asset you want to trade
        threshold_percentage = 0.02  # Percentage threshold for buy/sell signals

        # Execute the momentum trading strategy
        momentum_trading_strategy(symbol, threshold_percentage)

        # Sleep for a short period (e.g., 5 minutes) before checking again
        time.sleep(300)  # Sleep for 5 minutes
    except KeyboardInterrupt:
        print("Exiting the momentum trading bot.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(60)  # Wait 1 minute before retrying
