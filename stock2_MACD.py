# Import yfinance
import yfinance as yf
import matplotlib.pyplot as plt
from indicators import *
from tools import *
from tradingTools import *
import pandas as pd
from stockstats import StockDataFrame

# Get the data for stock Facebook from 2017-04-01 to 2019-04-30
# data = yf.download('MTY.TO', start="2022-10-01", end="2022-11-15", interval = "1d")

data = yf.download('MTY.TO', start="2022-09-10", end="2022-11-20", interval = "1d")

stocks = StockDataFrame.retype(data[["Open", "Close", "High", "Low", "Volume"]])
MACD = Indicator('MACD', colors['macd'], stocks['macd'])
MACDS = Indicator('MACDS', colors['macds'], stocks['macds'])
MACDH = Indicator('MACDH', colors['macdh'], stocks['macdh'])

BUY = cross(MACD, MACDS)
SELL = cross(MACDS, MACD)

DMI_ind = DMI(data)
# retype_data = StockDataFrame.retype(data[["Open", "Close", "High", "Low", "Volume"]])
# RSI = Indicator('RSI', colors['RSI'], retype_data['rsi'])

# Stochastic_indicator = Stochastic(data, 14)

# thresh_L = Threshold(30, data)
# thresh_H = Threshold(70, data)

# results = getResult(data, BUY, SELL, 0, commission=0.005)
# print(results)
# results.to_csv('results_essai_MTY.csv', header=True, index=True, encoding='utf-8')
getCharts(data, inChart2=[MACD, MACDS], inChart3=[DMI_ind], buySignals=BUY, sellSignals=SELL, showVolume=False)