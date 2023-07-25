from pybithumb import Bithumb
import pybithumb
import datetime
from Config import Config

#임계값 알고리즘
#가격 변동률 5% 이상 상승 시 매수
#가격 변동률 3% 이상 하락 시 매도
class Threshold_Algorithms:
    def __init__(self, ticker):
        self.ticker = ticker
        self.FEE = 500 # 수수료
        self.BUY_THRESHOLD = 0.05  # percentage change in price to trigger a buy signal
        self.SELL_THRESHOLD = -0.03  # percentage change in price to trigger a sell signal
        self.STOP_LOSS_THRESHOLD = -0.1  # percentage change in price to trigger a stop-loss sell
        self.
        
        self.buy_price = 0
        self.buy_time = ""
        self.holding = False
        self.bithumb = Bithumb(Config().ConnKey, Config().SecKey)
    
    def check_buy_signal(self, ticker, prev_price, curr_price):
        price_change = (curr_price - prev_price)/prev_price
        print("가격 변동률 : ", ticker, " : ", price_change*100, "%")
        if price_change > self.BUY_THRESHOLD:
            return True
        else : return False
    def check_sell_signal(self, ticker, curr_price, buy_price):
        price_change = (curr_price - buy_price)/buy_price
        print("가격 변동률 : ", ticker, " : ", price_change*100, "%")
        if price_change < self.SELL_THRESHOLD:
            return True
        elif price_change < self.STOP_LOSS_THRESHOLD:
            return True
        else : return False

    def getSignal(self, sendSignal):
        curr_price = float(Bithumb.get_current_price(self.ticker))
        curr_time = datetime.datetime.now()
        print(curr_time, " " , self.ticker , "가격 : " , str(curr_price))


        if self.holding==False:
            prev_price = float(pybithumb.get_ohlcv(self.ticker)['close'][-2])
            if self.check_buy_signal(self.ticker, prev_price,curr_price):
                krw = self.bithumb.get_balance(self.ticker)[2]-self.FEE
                orderBook = Bithumb.get_orderbook(self.ticker)
                sell_price = orderBook['asks'][0]['price']
                unit = krw/float(sell_price)

                sendSignal(['bid', self.ticker, unit]) #(bid|ask, ticker, unit)

                self.buy_price =  curr_price
                self.buy_time = curr_time

                print("[buy] unit : "+str(unit)+", buy_price: "+ str(curr_price) + "주문금액 : " + str(curr_price * unit))
                self.holding[self.ticker] = True
        else:
            if self.check_sell_signal(self.ticker, curr_price, self.buy_price):
                unit = self.bithumb.get_balance(self.ticker)[0]
                print("[sell buy signal] unit : "+ str(unit)+ ", sell_price : "+ str(curr_price))
                sendSignal(['ask', self.ticker, unit])
                self.holding = False
            elif (curr_time- self.buy_time).total_seconds() > 86400 :
                unit = self.bithumb.get_balance(self.ticker)[0]
                sendSignal(['ask', self.ticker, unit])
                print("[sell over 24hour] unit : "+ str(unit)+ ", sell_price : "+ str(curr_price))
                self.holding = False


