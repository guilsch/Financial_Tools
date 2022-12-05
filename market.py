from indicators import *
from tools import *
from tradingTools import *

import yfinance as yf
from stockstats import StockDataFrame

# Get the data for stock Facebook from 2017-04-01 to 2019-04-30
data = yf.download('^FCHI', start="2022-01-01", end="2022-09-30")

EMA20 = EMA(20, colors['red'])
EMA20.evaluate(data)
EMA50 = EMA(50, colors['blue'])
EMA50.evaluate(data)

getCharts(data, inChart1=[EMA20, EMA50])