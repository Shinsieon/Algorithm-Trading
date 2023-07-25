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
from Algorithms import Threshold_Algorithms
from AuthHeader import XCoinAPI
from Config import Config

form_class = uic.loadUiType("./CoinBot.ui")[0]

class BithumbBot(QMainWindow, form_class):
    def __init__(self):
        super(BithumbBot, self).__init__()
        self.setupUi(self)
        self.startBtn.clicked.connect(self.startBtnClicked)

    def closeEvent(self) :
        Event.set() #무한루프 종료시키기

    
    def startBtnClicked(self):
        self.addTradeLog("매매 시작")
        th1 = Thread(target=self.startTrade, args=())
        th1.start()

    def getMyAccount(self):
        CoinApi = XCoinAPI(Config().ConnKey, Config().SecKey)
        rgParams = {
            'endpoint': '/info/balance',  #<-- endpoint가 가장 처음으로 와야 한다.
            "currency": "ALL",
        }
        coins = CoinApi.xcoinApiCall(rgParams['endpoint'], rgParams)
        coinsHas = dict((key,value) for key, value in coins['data'].items() if key.startswith('available_') and float(value) > 0)
        return coinsHas #coinHas : {'available_krw': '50000.00000000'}
    
    #각 알고리즘은 tickers를 받아 매수, 매도 해야하는 코인 정보를 sendSignal 함수에 실어 보낸다.
    def startTrade(self):
        alg = Threshold_Algorithms('BTC')

        while True:
            if Event().is_set() : break #프로그램을 종료하면 무한루프도 같이 종료
            alg.getSignal(self.sendSignal) 
            myCoins = self.getMyAccount()
            self.addCoinLog(str(myCoins))

            time.sleep(2)
    
    #주문 클래스에 매수/매도 주문을 넣는다
    def sendSignal(self, sig):
        #sig = (bid|ask, ticker, unit, price)
        ord = Order()
        result = False
        if sig[0]=='bid' :
            result = ord.buy_coin(sig[1], sig[2])
        else : result = ord.sell_coin(sig[1], sig[2])

        if result: self.addTradeLog(str(sig[1]) + " " + str(sig[2]) + "개 " + str(sig[0]) + " 성공")
        else : self.addTradeLog(str(sig[1]) + " " + str(sig[2]) + "개 " + str(sig[0]) + " 실패")

    def addTradeLog(self, txt):
        print(txt)
        self.tradeLogListWidget.addItem(QListWidgetItem(txt))

    def addCoinLog(self, txt):
        self.budgetListWidget.addItem(QListWidgetItem(txt))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BithumbBot()

    window.show()

    sys.exit(app.exec())
