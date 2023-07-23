
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
from AuthHeader import XCoinAPI

ConnKey = 'aeedf9cff331bc3e2c1eabcfdffc22eb'
SecKey = '129255c8b8f61bf96754c225a3c8864d'
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        
    def initUI(self):
        self.setWindowTitle("CoinBot")
        container = QHBoxLayout()
        self.budgetListWidget = QListWidget()

        container.addWidget(self.budgetListWidget)

        startBtn = QPushButton("조회")
        startBtn.clicked.connect(self.startBtnClicked)

        container.addWidget(startBtn)

        self.setLayout(container)
        
    def startBtnClicked(self):
        myCoins = self.getMyBudget()
        print(myCoins)
        for coin in myCoins:
            self.budgetListWidget.addItem(QListWidgetItem(str(coin)+str(myCoins[coin])))

    def getMyBudget(self):
        CoinApi = XCoinAPI(ConnKey, SecKey)
        rgParams = {
            'endpoint': '/info/balance',  #<-- endpoint가 가장 처음으로 와야 한다.
            "currency": "ALL",
        }
        coins = CoinApi.xcoinApiCall(rgParams['endpoint'], rgParams)
        coinsHas = dict((key,value) for key, value in coins['data'].items() if key.startswith('available_') and float(value) > 0)
        return coinsHas

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.initUI()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 600,400
    window.setGeometry(int(size.width()/2-w/2), int(size.height()/2-h/2), w,h)
    window.show()

    app.exec()