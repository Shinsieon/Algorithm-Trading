
import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode,unquote
import requests
import time
import math

ACCESS_KEY = "eSEhc47xhGki7v0lB4C81fpqIsx8tWcDF5PWLNVs"
SECRET_KEY = "ZXFxFjR6JxLfvKzqyk9giFDMKKHRKgs6tIxAWMln"
SERVER_URL = "https://api.upbit.com"

class Api:
    def __init__(self):
        self.fuck = "hi"
        

    def upbitApi(self, url, type, params={}):
       
        #  params = {
        #     'market': 'KRW-BTC'
        #     }
        query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': ACCESS_KEY,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, SECRET_KEY)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {
        'Authorization': authorization,
        }
        if type=='get' : res = requests.get(SERVER_URL + url, headers=headers)
        else : res=  requests.post(SERVER_URL + url, json=params, headers = headers)
        return res.json()
    
    def getBudget(self):
        return self.upbitApi('/v1/accounts',"get", {})
    
    def getAllCoins(self):
        return list(filter(lambda x: x['market'].startswith('KRW'), self.upbitApi('/v1/market/all', "get" , {})))
    
    def getCoinSise(self, coin):
        return self.upbitApi('/v1/ticker?markets='+coin['market'], "get", {})

    def buyCoins(self,krwBalance, coins):
        budget_for_one_coin = math.floor(float(krwBalance)/len(coins))
        for coin in coins:
            price_of_coin = coin['trade_price']
            volume_of_coin = budget_for_one_coin/price_of_coin
            params = { 'market': coin['market'], 'side': 'bid', 'ord_type': 'price', 'price': budget_for_one_coin}
            print(params)
            res = self.upbitApi('/v1/orders/', "post" , params)
            print(res)
            
    def sellCoins(self, coin): #시장가 주문 매도(전량)
        price_of_coin = coin['trade_price']
        params = { 'market': 'KRW' + coin['currency'], 'side': 'ask', 'ord_type': 'market', 'volume' : coin['balance']}
        print(params)
        res = self.upbitApi('/v1/orders/', "post" , params)
        print(res)

    def getHogaInfo(self, coin):
        return self.upbitApi('/v1/orderbook?markets='+coin['market'], "get", {})