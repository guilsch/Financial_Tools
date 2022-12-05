from indicators import *
from tools import *
from tradingTools import *

import yfinance as yf
from stockstats import StockDataFrame

# Get the data for stock Facebook from 2017-04-01 to 2019-04-30
data = yf.download('TSLA', start="2022-09-20", end="2022-11-20", interval="1d")

thresh_L = Threshold(10, data)
thresh_H = Threshold(75, data)

DMI_indic = DMI(data)
DMIS = DMI_Stochastic(data)

[BUY, SELL] = getDMISSignals(DMIS, thresh_H, thresh_L)

stocks = StockDataFrame.retype(data[["Open", "Close", "High", "Low", "Volume"]])
RSI = Indicator('RSI', colors['RSI'], stocks['rsi'])
MACD = Indicator('MACD', colors['macd'], stocks['macd'])


getResult(data, BUY, SELL, maxStock=10, minStock=-10)
getCharts(data, inChart2=[DMI_indic], inChart3=[thresh_L, thresh_H, DMIS], buySignals=BUY, sellSignals=SELL)
# getCharts(data)