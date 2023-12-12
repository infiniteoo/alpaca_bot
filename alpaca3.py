import alpaca_trade_api as api
import pandas as pd
from datetime import datetime, timedelta, timezone
import yfinance as yf
import os
from dotenv import load_dotenv
import requests
import json
import time
from Colors import Colors as c
import sys
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Load environment variables
load_dotenv()

# Read the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Alpaca API credentials
API_KEY = os.getenv('TRADER_KEY')
API_SECRET = os.getenv('TRADER_SECRET')
BASE_URL = os.getenv('TRADER_ENDPOINT')  # Paper trading URL
account_id = os.getenv('ACCOUNT_ID')

symbol = config["symbol"]
short_window = config["short_window"]
long_window = config["long_window"]
lookback = config["lookback"]


api = TradingClient(f'{API_KEY}', f'{API_SECRET}')


# Function to print account details
def print_account_details():
    try:
        # Get our account information.
        account = api.get_account()

        # Check if our account is restricted from trading.
        if account.trading_blocked:
            print('Account is currently restricted from trading.')

        # Check how much money we can use to open new positions.
        print('${} is available as buying power.'.format(account.buying_power))
        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')
    except Exception as e:
        print(f"Error fetching account details: {e}")

# Function to print current positions
def print_current_positions():
    try:
        # Get a list of all of our positions.
        portfolio =  api.get_all_positions()  
        for position in portfolio:
            print("{} shares of {}".format(position.qty, position.symbol))
        if not portfolio:
            print("You don't have any positions.")   
    except Exception as e:
        print(f"Error fetching current positions: {e}")

# Function to check if the market is open
def is_market_open():
    try:
       # Get the market clock
        clock = api.get_clock()
           
        # Check if the market is open
        if clock.is_open:
            print("The market is open.")
            print(f"Next market open: {clock.next_open}")
            print(f"Next market close: {clock.next_close}")
        else:
            print("The market is closed.")
            print(f"Next market open: {clock.next_open}")
            return clock.is_open
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False

# Get historical data from Yahoo Finance
def get_historical_data(symbol):
    ticker_symbol = symbol.upper()
    now = datetime.now()
    start_date = now - timedelta(days=lookback)  # Adjust as needed

    try:
        # Request historical data from Alpaca
        historical_data = api.get_barset(
            symbols=[ticker_symbol],
            timeframe='day',
            start=start_date,
            end=now
        )[ticker_symbol]

        # Convert the data to a DataFrame
        data = pd.DataFrame({
            'Open': [bar.o for bar in historical_data],
            'High': [bar.h for bar in historical_data],
            'Low': [bar.l for bar in historical_data],
            'Close': [bar.c for bar in historical_data],
            'Volume': [bar.v for bar in historical_data]
        })

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
    if not is_market_open():  # Check if market is open
        print(f"{c.RED}Market is not open. Skipping trade execution. {c.RESET}")
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

        # Check your existing position for the symbol
        existing_position = api.get_position(symbol)

        if existing_position is not None and int(existing_position.qty) >= 1:
            print(f"You already own {existing_position.qty} shares of {symbol}. Skipping buy order.")
            return

        try:
            # Place a market order to buy 3 shares of the symbol
            api.submit_order(
                symbol=symbol,
                qty=3,
                side='buy',
                type='market',
                time_in_force='gtc'  # Good Till Cancelled
            )
            print("Buy order placed successfully.")
        except Exception as e:
            print(f"Error placing buy order: {e}")
    elif latest_data['Short_MA'] < latest_data['Long_MA']:  
        # Sell signal
        print(f"Sell signal for {symbol}")
        # Check your existing position for the symbol
        existing_position = api.get_position(symbol)

        if existing_position is None:
            print(f"You don't own any shares of {symbol}. Skipping sell order.")
            return

        if existing_position is not None and int(existing_position.qty) <= 3:
            print(f"Selling {existing_position.qty} shares of {symbol}...")
            return
        try:
            # Place a market order to sell 3 shares of the symbol
            api.submit_order(
                symbol=symbol,
                qty=int(existing_position.qty) | 3,
                side='sell',
                type='market',
                time_in_force='gtc'  # Good Till Cancelled
            )
            print("Sell order placed successfully.")
        except Exception as e:
            print(f"Error placing sell order: {e}")



interval_seconds = 15  
next_run_time = time.time() + interval_seconds

# Main loop
while True:
    try:
       

        time_remaining = next_run_time - time.time()
        print(f"Time until next loop: {int(time_remaining)} seconds", end='\r')
        sys.stdout.flush()


        if time_remaining <= 0:
            # Reset the next run time and execute the main logic
            next_run_time = time.time() + interval_seconds
             # Print account and position details
            print_account_details()
            print_current_positions()

            # Run the strategy
            moving_average_strategy(symbol, short_window, long_window)
        else:
            time.sleep(1) 
        
    except KeyboardInterrupt:
        print(f"{c.RED}Exiting the trading bot.{c.RESET}")
        break
    except Exception as e:
        print(f"{c.RED}An error occurred: {e}{c.RESET}")
        time.sleep(300)  # Wait before retrying