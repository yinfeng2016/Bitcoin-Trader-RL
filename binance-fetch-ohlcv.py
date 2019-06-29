# -*- coding: utf-8 -*-

import os
import sys
import datetime
import pandas as pd
import csv
import time
# import asciichart

# -----------------------------------------------------------------------------

# this_folder = os.path.dirname(os.path.abspath(__file__))
# root_folder = os.path.dirname(os.path.dirname(this_folder))
# sys.path.append(root_folder + '/python')
# sys.path.append(this_folder)

# -----------------------------------------------------------------------------

import ccxt  # noqa: E402

# -----------------------------------------------------------------------------

binance = ccxt.binance()
# symbol = 'BTC/USDT'
# timeframe = '1h'

# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
# index = 4  # use close price from each ohlcv candle

# height = 15
# length = 80


# def print_chart(exchange, symbol, timeframe):

#     # print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

#     # get a list of ohlcv candles
#     ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

#     # get the ohlCv (closing price, index == 4)
#     # series = [x[index] for x in ohlcv]

#     # print the chart
#     # print("\n" + asciichart.plot(series[-length:], {'height': height}))  # print the chart

#     last = ohlcv[len(ohlcv) - 1]  # last closing price
#     return last


# last = print_chart(binance, symbol, timeframe)
ohlcv = binance.fetch_ohlcv('BTC/USDT', '1h')
last = ohlcv[len(ohlcv) - 1]
# date = datetime.datetime.fromtimestamp(last[0]/1000.0)
# date = date.strftime('%Y-%m-%d %H:%M:%S')
print(ohlcv[0][0])  # print last closing price


df = pd.read_csv('binance.csv')
# # df = df.drop(['Symbol'], axis=1)
df = df.sort_values(['Date'])
# # print (df)
# print(df.iloc[-1].values[0])


# -----------------------------------------------------------------------------

def scrape_ohlcv(exchange, symbol, timeframe, filename, df):
    while True:
         # if we have reached the beginning of history
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, exchange.milliseconds()-7200000)
        # print(exchange.milliseconds())
        print(ohlcv)
        time.sleep(5)
        # if df.iloc[-1].values[0] >= ohlcv[0][0] - 3600000:
        #     time.sleep(60)
        # if we have reached the checkpoint
        df = pd.read_csv('binance.csv')
        df = df.sort_values(['Date'])
        if ohlcv[0][0] > df.iloc[-1].values[0]:
            write_to_csv(filename, ohlcv[0])

    return ohlcv

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(data)
    output_file.close


def scrape_candles_to_csv(filename, exchange_id, symbol, timeframe):
    # instantiate the exchange by id
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,  # required by the Manual
    })
    # convert since from string to milliseconds integer if needed

    # preload all markets from the exchange
    exchange.load_markets()
    # fetch all candles
    ohlcv = scrape_ohlcv(exchange, symbol, timeframe, filename, df)
    # save them to csv file
    print('Saved', len(ohlcv), 'candles' 'to', filename)


# -----------------------------------------------------------------------------

scrape_candles_to_csv('binance.csv', 'binance', 'BTC/USDT', '1h')
