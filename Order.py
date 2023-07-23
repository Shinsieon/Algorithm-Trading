from pybithumb import Bithumb
from Config import Config
class Order:
    def __init__(self):
        super(self)
        self.bithumb = Bithumb(Config().ConnKey, Config().SecKey)

    def buy_coin(self, ticker, unit):
        try:
            self.bithumb.buy_market_order(ticker, unit)
            return True
        except:
            return False
    
    def sell_coin(self,ticker, unit):
        try:
            self.bithumb.sell_market_order(ticker,unit)
            return True
        except:
            return False
