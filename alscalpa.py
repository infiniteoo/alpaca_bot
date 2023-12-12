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

# Scalping strategy
def scalping_strategy(symbol, target_profit, stop_loss, max_trades_per_day):
    if not is_market_open():
        print("Market is closed. Skipping trade execution.")
        return

    # Check the current time
    current_time = api.get_clock().timestamp
    trading_start_time = current_time.replace(hour=9, minute=30, second=0, microsecond=0)
    trading_end_time = current_time.replace(hour=15, minute=59, second=0, microsecond=0)

    if not trading_start_time <= current_time <= trading_end_time:
        print("Outside of trading hours. Skipping trade execution.")
        return

    # Check the number of trades executed today
    trades_today = len(api.list_orders(status='filled', limit=100))
    if trades_today >= max_trades_per_day:
        print("Maximum daily trades reached. Skipping trade execution.")
        return

    # Get the current price
    current_price = api.get_latest_trade(symbol=symbol).price

    # Calculate the profit and loss thresholds
    take_profit = current_price * (1 + target_profit)
    stop_loss_price = current_price * (1 - stop_loss)

    # Place a limit order to sell at the take profit level
    api.submit_order(
        symbol=symbol,
        qty=1,
        side='sell',
        type='limit',
        time_in_force='gtc',
        limit_price=take_profit
    )

    # Place a stop loss order to limit losses
    api.submit_order(
        symbol=symbol,
        qty=1,
        side='sell',
        type='stop',
        time_in_force='gtc',
        stop_price=stop_loss_price
    )

    print(f"Scalping {symbol} at ${current_price} (Target: ${take_profit}, Stop Loss: ${stop_loss_price})")

# Main loop
while True:
    try:
        # Define your scalping parameters
        symbol = ' URNM'  # The stock you want to scalp
        target_profit = 0.005  # 0.5% target profit
        stop_loss = 0.003  # 0.3% stop loss
        max_trades_per_day = 3  # Maximum trades per day

        # Execute the scalping strategy
        scalping_strategy(symbol, target_profit, stop_loss, max_trades_per_day)

        # Sleep for a short time before checking again (e.g., 5 minutes)
        time.sleep(300)
    except KeyboardInterrupt:
        print("Exiting the scalping bot.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(300)  # Wait before retrying
