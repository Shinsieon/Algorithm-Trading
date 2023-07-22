import sys
from PyQt6.QtWidgets import *
from Order import Order
from Api import Api
from PyQt6 import uic
from threading import Thread
import schedule

form_class = uic.loadUiType("./CoinBot.ui")[0]


class CoinBot(QMainWindow, form_class):
    def __init__(self):
        super(CoinBot, self).__init__()
        self.setupUi(self)
        self.BUY_THRESHOLD = 0.05  # percentage change in price to trigger a buy signal
        self.SELL_THRESHOLD = (
            -0.03
        )  # percentage change in price to trigger a sell signal
        self.STOP_LOSS_THRESHOLD = -0.1
        self.krwBalance = 0
        self.coins = {}  # coin 시세 저장

        self.budgets = Api().getBudget()
        self.setMyBuggetsView()

        self.startBtn.clicked.connect(self.startBtnClicked)

        schedule.every(1).minutes.do(self.sell_coins)

    def sell_coins(self):
        if len(self.coins)>0 and len(self.budgets)>0 :
            for budget in self.budgets :
                if budget['currency'] == 'KRW' : pass
                if self.check_sell_signal(budget['avg_buy_price'], self.coins['KRW' + budget['currency']]) == True:
                    Api().sellCoin(budget)

    def setMyBuggetsView(self):
        print(self.budgets)
        for budget in self.budgets:
            budgetLbl = QListWidgetItem(budget["currency"] + " " + budget["balance"])
            if budget["currency"] == "KRW":
                self.krwBalance = budget["balance"]
            self.budgetListWidget.addItem(budgetLbl)

    def startBtnClicked(self):
        coins = Api().getAllCoins()
        print(coins)
        th1 = Thread(target=self.getAllCoinSise, args=(coins,))
        self.addTradeLog("코인 시세를 조회중입니다.")
        th1.start()
        th1.join()
        # self.getAllCoinSise(coins)

        sorted_coins_by_trade_volume = sorted(
            self.coins, key=lambda item: item["trade_volume"], reverse=True
        )[0:5]
        Api().buyCoins(self.krwBalance, sorted_coins_by_trade_volume)

        for coin in sorted_coins_by_trade_volume:
            self.addTradeLog(
                coin["market"]
                + " | "
                + str(coin["opening_price"])
                + " | "
                + str(coin["trade_volume"])
            )

    def getAllCoinSise(self, coins):
        self.coins = {}
        for coin in coins:
            try:
                sise = Api().getCoinSise(coin)
                # hoga = Api().getHogaInfo(coin)
                # print(hoga)
                self.coins[coin['market']] = sise[0]
                # break
            except:
                pass

    # def check_can_buy_coins(self, coins):

    def check_sell_signal(self, prev_price, curr_price):
        price_change = (curr_price - prev_price) / prev_price
        return True if price_change <= self.SELL_THRESHOLD else False

    def addTradeLog(self, txt):
        self.tradeLogListWidget.addItem(QListWidgetItem(txt))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoinBot()

    window.show()

    app.exec()
