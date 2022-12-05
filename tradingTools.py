from signal import signal
import pandas as pd
import numpy as np
import yfinance as yf
from indicators import *
from tools import getDfFromAny
from math import isnan

def cross(indicator1, indicator2):
    
    df1 = getDfFromAny(indicator1)
    df2 = getDfFromAny(indicator2)
    
    signals = pd.DataFrame(index = df1.index)
    signals['Signal'] = 0
    
    for i in range(df1.shape[0]):
        if i > 0 and not isnan(df1[i]) and not isnan(df1[i-1]) and not isnan(df2[i]) and not isnan(df2[i-1]):
            if df1[i] >= df2[i] and df1[i-1] < df2[i-1]:
                signals['Signal'][i] = 1
            
    return Indicator('cross', '#aaaaaa', data=signals)

def getDMISSignals(DMIS, HighThresh, LowThresh):
    
    DMIS_df = getDfFromAny(DMIS)
    DMI_df = getDfFromAny(DMIS.DMI)
    
    overboughtSignals_df = getDfFromAny(cross(DMIS, HighThresh))
    oversoldSignals_df = getDfFromAny(cross(LowThresh, DMIS))
    oversoldSignals_df['Signal'] = 0
    
    buys_df = pd.DataFrame(index = DMIS_df.index)
    buys_df['Signal'] = 0
    sells_df = pd.DataFrame(index = DMIS_df.index)
    sells_df['Signal'] = 0
    
    for i in range(DMIS_df.shape[0]):
        
        if overboughtSignals_df[i] == 1 and DMI_df[i] < 0:
            sells_df['Signal'][i] = 1
        
        if oversoldSignals_df[i] == 1 and DMI_df[i] > 0:
            buys_df['Signal'][i] = 1
    
    return Indicator('cross', '#aaaaaa', data=buys_df), Indicator('cross', '#aaaaaa', data=sells_df)

def getCCIsignals(CCI, Thresh_H, Thresh_L):
    
    ccidf = getDfFromAny(CCI)
    threshHdf = getDfFromAny(Thresh_H)
    threshLdf = getDfFromAny(Thresh_L)
    
    buys = pd.DataFrame(index = ccidf.index)
    buys['Signal'] = 0
    sells = pd.DataFrame(index = ccidf.index)
    sells['Signal'] = 0
    
    for i in range(ccidf.shape[0]):
        if i > 0 and not isnan(ccidf[i]) and not isnan(ccidf[i-1]):
            
            if ccidf[i] >= threshHdf[i] and ccidf[i-1] < threshHdf[i-1]:
                buys['Signal'][i] = 1
            
            if ccidf[i] <= threshHdf[i] and ccidf[i-1] > threshHdf[i-1]:
                sells['Signal'][i] = 1
                
            if ccidf[i] <= threshLdf[i] and ccidf[i-1] > threshLdf[i-1]:
                sells['Signal'][i] = 1
                
            if ccidf[i] >= threshLdf[i] and ccidf[i-1] < threshLdf[i-1]:
                buys['Signal'][i] = 1
                
    return Indicator('CCI Signals buys', '#aaaaaa', data=buys), Indicator('CCI Signals sells', '#aaaaaa', data=sells)