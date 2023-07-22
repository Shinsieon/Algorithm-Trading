class Order:
    def __init__(self):
        super(self)

    def buy_coins(self, myBalance, coins):
        print(myBalance) #원금을 등분한 금액만큼 매수.
        
        # budget_for_one_coin = float(self.krwBalance)/len(coins)
        # for coin in coins:
        #     price_of_coin = coin['trade_price']
        #     volume_of_coin = budget_for_one_coin/price_of_coin
        #     params = { 'market': coin['market'], 'side': 'bid', 'ord_type': 'price', 'price': price_of_coin, 'volume': volume_of_coin}
        #     self.upbitApi('/v1/orders/', "post" , params)


        #test = [{'market': 'KRW-BTC', 'trade_date': '20230722', 'trade_time': '024228', 'trade_date_kst': '20230722', 'trade_time_kst': '114228', 'trade_timestamp': 1689993748466, 'opening_price': 38838000.0, 'high_price': 38934000.0, 'low_price': 38750000.0, 'trade_price': 38796000.0, 'prev_closing_price': 38829000.0, 'change': 'FALL', 'change_price': 33000.0, 'change_rate': 0.0008498802, 'signed_change_price': -33000.0, 'signed_change_rate': -0.0008498802, 'trade_volume': 0.02045305, 'acc_trade_price': 9184721497.5086, 'acc_trade_price_24h': 73460308428.86922, 'acc_trade_volume': 236.40970954, 'acc_trade_volume_24h': 1897.63903665, 'highest_52_week_price': 41569000.0, 'highest_52_week_date': '2023-06-30', 'lowest_52_week_price': 20700000.0, 'lowest_52_week_date': '2022-12-30', 'timestamp': 1689993748494}]