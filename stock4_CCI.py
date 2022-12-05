from indicators import *
from tools import *
from tradingTools import *

import yfinance as yf
from stockstats import StockDataFrame

# Get the data for stock Facebook from 2017-04-01 to 2019-04-30
data = yf.download('CAT', start="2010-01-01", end="2022-09-30", interval="1d")

thresh_L = Threshold(-100, data)
thresh_H = Threshold(100, data)

retype_data = StockDataFrame.retype(data[["Open", "Close", "High", "Low", "Volume"]])
CCI = Indicator('CCI', colors['blue'], retype_data['cci'])

EMA_short = EMA(5, '#ff207c')
EMA_short.evaluate(data)

EMA_long = EMA(20, '#ffa320')
EMA_long.evaluate(data)

BUY, SELL = getCCIsignals(CCI, Thresh_H=thresh_H, Thresh_L=thresh_L)

getCharts(data)

# results = getResult(data, BUY, SELL, maxStock=1, minStock=-1, stockNB=1, commission=0.005)
# results.to_csv('results_essai_CAT.csv', header=True, index=True, encoding='utf-8')
# getCharts(data, inChart1=[EMA_short, EMA_long], inChart2=[CCI, thresh_H, thresh_L], buySignals=BUY, sellSignals=SELL)