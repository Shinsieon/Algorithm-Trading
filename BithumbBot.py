import sys
from PyQt6.QtWidgets import *
from Order import Order
from Api import Api
from PyQt6 import QtGui, uic
from threading import Thread, Event
from pybithumb import Bithumb
import datetime
import time
import pybithumb
import pandas as pd

form_class = uic.loadUiType("./CoinBot.ui")[0]
ConnKey = 'aeedf9cff331bc3e2c1eabcfdffc22eb'
SecKey = '129255c8b8f61bf96754c225a3c8864d'
class BithumbBot(QMainWindow, form_class):
    def __init__(self):
        super(BithumbBot, self).__init__()
        self.setupUi(self)
        self.BUY_THRESHOLD = 0.05  # percentage change in price to trigger a buy signal
        self.SELL_THRESHOLD = -0.03  # percentage change in price to trigger a sell signal
        self.STOP_LOSS_THRESHOLD = -0.1  # percentage change in price to trigger a stop-loss sell

        self.bithumb = Bithumb(ConnKey, SecKey)
        self.ticker = 'BTC'
        self.holding = False
        self.buy_all(self.ticker)

        self.startBtn.clicked.connect(self.startBtnClicked)

    def closeEvent(self) :
        Event.set() #무한루프 종료시키기


    def check_buy_signal(self, prev_price, curr_price):
        price_change = (curr_price - prev_price)/prev_price
        self.addTradeLog("가격변동율 : " + str(price_change))
        if price_change > self.BUY_THRESHOLD:
            return True
        else : return False
    def check_sell_signal(self, curr_price, buy_price):
        price_change = (curr_price - buy_price)/buy_price
        self.addTradeLog("가격변동율 : " + str(price_change))
        if price_change < self.SELL_THRESHOLD:
            return True
        elif price_change < self.STOP_LOSS_THRESHOLD:
            return True
        else : return False
    
    def buy_all(self,ticker):
        krw = self.bithumb.get_balance(ticker)[2]
        #get_balance return (0.0, 0.0, 50000.0, 0.0)
        orderBook = Bithumb.get_orderbook(ticker)
        sell_price = orderBook['asks'][0]['price']
        unit = krw/float(sell_price)
        self.bithumb.buy_market_order(ticker, unit)
        return unit
    
    def sell_all(self,ticker):
        unit = self.bithumb.get_balance(ticker)[0]
        self.bithumb.sell_market_order(ticker,unit)
        return unit
    
    def startBtnClicked(self):
        th1 = Thread(target=self.startTrade, args=())
        #self.th1.daemon = True
        th1.start()
        self.tradeLogListWidget.addItem(QListWidgetItem("매매 시작"))
    def startTrade(self):
        while True:
            if Event().is_set() : break
            curr_price = float(Bithumb.get_current_price(self.ticker))
            self.addTradeLog(self.ticker + "가격 : " + str(curr_price))
            curr_time = datetime.datetime.now()

            self.addTradeLog(str(curr_time)+ '|' + str(curr_price))
            self.addTradeLog("현재 자산 " +str(self.bithumb.get_balance(self.ticker)[2]))

            if self.holding==False:
                prev_price = float(pybithumb.get_ohlcv(self.ticker)['close'][-2])
                if self.check_buy_signal(prev_price,curr_price):
                    unit = self.buy_all(self.ticker)
                    buy_price = curr_price
                    buy_time = curr_time
                    self.addTradeLog("[buy] unit : "+str(unit)+", buy_price: "+ str(curr_price))
                    self.holding = True
            else:
                if self.check_sell_signal(curr_price, buy_price):
                    unit = self.sell_all(self.ticker)
                    self.addTradeLog("[sell buy signal] unit : "+ str(unit)+ ", sell_price : "+ str(curr_price))
                    self.holding = False
                elif (curr_time- buy_time).total_seconds() > 86400 :
                    unit = self.sell_all(self.ticker)
                    self.addTradeLog("[sell over 24hour] unit : "+ str(unit)+ ", sell_price : "+ str(curr_price))
                    self.holding = False


            time.sleep(5)

    def addTradeLog(self, txt):
        print(txt)
        self.tradeLogListWidget.addItem(QListWidgetItem(txt))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BithumbBot()

    window.show()

    sys.exit(app.exec())
