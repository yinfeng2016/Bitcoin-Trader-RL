# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
type = 'limit'  # or 'market'
side = 'buy'  # or 'buy'
amount = 0.02
price = 10650  # or None

# extra params and overrides if needed
# params = {
#     'test': True,  # test if it's valid, but don't actually place it
# }

order = exchange.create_order(symbol, type, side, amount, price, params)

print(order)