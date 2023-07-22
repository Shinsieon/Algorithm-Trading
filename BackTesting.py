class BackTesting:
    def __init__(self, start_cash):
        self.start_cash = start_cash
        self.ror_list = []
        self.buy_count = 0
        self.sell_count = 0
        self.sell_count_by_timeout = 0
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0
        self.curr_price = 0
        self.highest_price = -float('inf')
        self.lowest_price = float('inf')
        self.holding = False
        self.buy_price = 0

    def curr_record(self, curr_price):
        self.curr_price = curr_price

        if self.curr_price > self. highest_price:
            self.highest_price = self.curr_price
        if self.curr_price < self.lowest_price:
            self.lowest_price = self.curr_price

    def buy_record(self, curr_price):
        self.buy_count += 1
        self.holding = True
        self.buy_price = curr_price

    def sell_record(self, timeout):
        self.sell_count +=1 
        if timeout == True:
            self.sell_count_by_timeout +=1

        #Rate of Return
        ror = float(self.curr_price) / float(self.buy_price)
        self.ror_list.append(ror)

    def print_report(self):
        print("count buy sell timeout_sell : " , self.buy_count, self.sell_count, self.sell_count_by_timeout)

        current_balance = self.start_cash
        highest_balance = self.start_cash
        lowest_balance = self.start_cash

        #Holding Period Return : 기간 수익률 : 수익률을 모두 곱한 것
        hpr = 1

        for ror in self.ror_list:
            if ror> 1.0:
                self.win_count +=1 
            elif ror==1.0:
                self.draw_count +=1
            else :
                self.lose_count +=1 

            hpr *= ror
            current_balance *= ror

            if current_balance > highest_balance:
                highest_balance = current_balance
            if current_balance < lowest_balance:
                lowest_balance = current_balance
            
        print('count win draw lose :', self.win_count, self.draw_count, self.lose_count)
        print('winning rate : {:.4f}'.format(self.win_count / (self.win_count + self.draw_count + self.lose_count)))

        print('start cash :', self.start_cash)
        print('balance curr high low : {0:.4f} {1:.4f} {2:.4f}'.format(current_balance, highest_balance, lowest_balance))
        print('Maximum Drawdown : {:.4f}'.format((highest_balance - lowest_balance) / highest_balance))
        print('Holding period return : {:.4f}'.format(hpr))