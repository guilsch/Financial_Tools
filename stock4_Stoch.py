from indicators import *
from tools import *
from tradingTools import *

import yfinance as yf
from stockstats import StockDataFrame

# Get the data for stock Facebook from 2017-04-01 to 2019-04-30
data = yf.download('RNO.PA', start="2022-09-01", end="2022-11-20")

thresh_L = Threshold(35, data)
thresh_H = Threshold(80, data)

Stochastic_indicator = Stochastic(data, 14)
DMI_indic = DMI(data)

BUY = cross(thresh_L, Stochastic_indicator)
SELL = cross(Stochastic_indicator, thresh_H)

results = getResult(data, BUY, SELL, maxStock=10, minStock=-10, stockNB=1, commission=0.005)
# results.to_csv('results_essai_RNO.csv', header=True, index=True, encoding='utf-8')
getCharts(data, inChart2=[Stochastic_indicator, thresh_H, thresh_L], inChart3=[DMI_indic], buySignals=BUY, sellSignals=SELL)