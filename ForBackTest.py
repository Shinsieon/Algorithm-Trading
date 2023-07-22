import pybithumb
import pandas as pd

from BackTesting import BackTesting

print("this is for backtest")

bt = BackTesting(100)

ticker = 'BTC'

BUY_THRESHOLD = 0.05  # percentage change in price to trigger a buy signal
SELL_THRESHOLD = -0.03  # percentage change in price to trigger a sell signal
STOP_LOSS_THRESHOLD = -0.1  # percentage change in price to trigger a stop-loss sell

def check_buy_signal(ticker, prev_price, curr_price):
    #previous_price = pybithumb.get_ohlcv(ticker)['close'][-2]  # get previous closing price
    price_change = (curr_price - prev_price) / prev_price  # calculate price change percentage

    if price_change > BUY_THRESHOLD:
        return True
    else:
        return False

def check_sell_signal(ticker, curr_price, buy_price):
    price_change = (curr_price - buy_price) / buy_price  # calculate price change percentage

    if price_change < SELL_THRESHOLD:
        return True  # sell if the price has dropped by the sell threshold percentage
    elif price_change < STOP_LOSS_THRESHOLD:
        return True  # sell if the price has dropped by the stop loss threshold percentage
    else:
        return False
    
# retrieve historical data
df = pybithumb.get_ohlcv(ticker, interval='day')
print(df)

# initialize variables
holding = False
buy_price = 0
buy_time = None

# iterate over the historical data
for i in range(1, len(df)):
    curr_price = df.iloc[i]['close']
    prev_price = df.iloc[i-1]['close']
    curr_time = df.index[i]

    bt.curr_record(curr_price)
    
    if holding == False:
        if check_buy_signal(ticker, prev_price, curr_price):
            bt.buy_record(curr_price)
            buy_price = curr_price
            buy_time = curr_time
            holding = True
    else:
        if check_sell_signal(ticker, curr_price, buy_price):
            holding = False
            bt.sell_record(False)
        elif (curr_time - buy_time).total_seconds() > 86400*2:
            holding = False
            bt.sell_record(True)

# calculate final holding period return
if holding:
    bt.sell_record(True)
    
bt.print_report()  