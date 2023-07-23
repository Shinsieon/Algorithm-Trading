from pybithumb import Bithumb
import pybithumb
import datetime
from Config import Config

#임계값 알고리즘
#가격 변동률 5% 이상 상승 시 매수
#가격 변동률 3% 이상 하락 시 매도
class Threshold_Algorithms:
    def __init__(self, tickers):
        self.tickers = tickers
        self.BUY_THRESHOLD = 0.05  # percentage change in price to trigger a buy signal
        self.SELL_THRESHOLD = -0.03  # percentage change in price to trigger a sell signal
        self.STOP_LOSS_THRESHOLD = -0.1  # percentage change in price to trigger a stop-loss sell
        self.buy_price = {}
        self.buy_time = {}
        self.holding = {}
        for ticker in tickers : self.holding[ticker] = False
        self.bithumb = Bithumb(Config().ConnKey, Config().SecKey)
    
    def check_buy_signal(self, prev_price, curr_price):
        price_change = (curr_price - prev_price)/prev_price
        if price_change > self.BUY_THRESHOLD:
            return True
        else : return False
    def check_sell_signal(self, curr_price, buy_price):
        price_change = (curr_price - buy_price)/buy_price
        if price_change < self.SELL_THRESHOLD:
            return True
        elif price_change < self.STOP_LOSS_THRESHOLD:
            return True
        else : return False

    def getSignal(self, sendSignal):
        for ticker in self.tickers:
            curr_price = float(Bithumb.get_current_price(ticker))
            print(ticker + "가격 : " + str(curr_price))
            curr_time = datetime.datetime.now()

            print(str(curr_time)+ '|' + str(curr_price))

            if self.holding[ticker]==False:
                prev_price = float(pybithumb.get_ohlcv(ticker)['close'][-2])
                if self.check_buy_signal(prev_price,curr_price):
                    krw = self.bithumb.get_balance(ticker)[2]
                    orderBook = Bithumb.get_orderbook(ticker)
                    sell_price = orderBook['asks'][0]['price']
                    unit = krw/float(sell_price)

                    sendSignal(['bid', ticker, unit]) #(bid|ask, ticker, unit)

                    self.buy_price[ticker] = curr_price
                    self.buy_time[ticker] = curr_time

                    print("[buy] unit : "+str(unit)+", buy_price: "+ str(curr_price))
                    self.holding[ticker] = True
            else:
                if self.check_sell_signal(curr_price, self.buy_price[ticker]):
                    unit = self.bithumb.get_balance(ticker)[0](ticker)
                    print("[sell buy signal] unit : "+ str(unit)+ ", sell_price : "+ str(curr_price))
                    sendSignal(['ask', ticker, unit])
                    self.holding[ticker] = False
                elif (curr_time- self.buy_time[ticker]).total_seconds() > 86400 :
                    unit = self.bithumb.get_balance(ticker)[0](ticker)
                    sendSignal(['ask', ticker, unit])
                    print("[sell over 24hour] unit : "+ str(unit)+ ", sell_price : "+ str(curr_price))
                    self.holding[ticker] = False


