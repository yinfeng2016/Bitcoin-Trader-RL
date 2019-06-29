# -*- coding: utf-8 -*-

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


exchange = ccxt.binance({
    'apiKey': '5QlpHnlZC8AT5pKfKhmPVbVvreRlggyWG25Tcq0JojH6EMcz8M9cEpz4SpEfOlM2',
    'secret': 'MnQAISsqQxzDQTpn5vJEwmurMXDKbFzpBobuanGy5xyK6aEJUod2bDmG98xdTdxF',
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
type = 'limit'  # or 'market'
side = 'sell'  # or 'buy'
amount = 1.0
price = 10086  # or None

# extra params and overrides if needed
params = {
    'test': True,  # test if it's valid, but don't actually place it
}

order = exchange.create_order(symbol, type, side, amount, price, params)

print(order)
