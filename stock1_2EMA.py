# Import yfinance
import yfinance as yf
import matplotlib.pyplot as plt
from indicators import *
from tools import *
from tradingTools import *
import pandas as pd
from stockstats import StockDataFrame

# Get the data for stock Facebook from 2017-04-01 to 2019-04-30
data = yf.download('AAPL', start="2022-09-25", end="2022-11-20", interval = "1h")

# # Calculate exponential moving average
EMA_short = EMA(5, '#ff207c')
EMA_short.evaluate(data)

EMA_long = EMA(30, '#ffa320')
EMA_long.evaluate(data)

retype_data = StockDataFrame.retype(data[["Open", "Close", "High", "Low", "Volume"]])
RSI = Indicator('RSI', colors['green'], retype_data['rsi'])

buy = cross(EMA_short, EMA_long)
sell = cross(EMA_long, EMA_short)

results = getResult(data, buy, sell, 0, stockNB=1, commission=0.005)
# print(results)
# results.to_csv('results.csv', header=True, index=True, encoding='utf-8')
getCharts(data, buySignals=buy, sellSignals=sell, inChart1=[EMA_short, EMA_long], inChart2=[RSI], showVolume=False)
# getCharts(data)