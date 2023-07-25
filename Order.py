from pybithumb import Bithumb
from Config import Config
import math
class Order:
    def __init__(self):
        self.bithumb = Bithumb(Config().ConnKey, Config().SecKey)

    def buy_coin(self, ticker, unit):
        try:
            res = self.bithumb.buy_market_order(ticker, unit)
            print(res)
            return True
        except:
            return False
    
    def sell_coin(self,ticker, unit):
        try:
            res = self.bithumb.sell_market_order(ticker,unit)
            print(res)
            return True
        except:
            return False
