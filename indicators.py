from audioop import avg
from colorsys import hsv_to_rgb
from statistics import mean
from stockstats import StockDataFrame
import pandas as pd


class Indicator:
    def __init__(self, name = "", color="#000000", data = None, inLegend=True):
        self.name = name
        self.data = data
        self.color = color
        self.inLegend = inLegend
        

class Threshold(Indicator):
    ### Create a series with one value ###
    def __init__(self, value, refDF, color='#ff0000'):
        super().__init__('threshold', color, inLegend=False)
        self.data = self.evaluate(value, refDF)
        
    def evaluate(self, value, refDF):
        data = pd.DataFrame(index = refDF.index)
        data['data'] = value
        self.data = data
        return data


class EMA(Indicator):
    def __init__(self, period, color):
        super().__init__('SMA-' + str(period), color)
        self.period = period

    def evaluate(self, stockDF):
        self.data = stockDF.Close.ewm(span=self.period, adjust=False).mean()


class DMI(Indicator):
    def __init__(self, stockDF, color='#000000'):
        super().__init__('DMI', color)
        self.data = self.evaluate(stockDF)

    def evaluate(self, stockDF):
        stocks = StockDataFrame.retype(
            stockDF[["Open", "Close", "High", "Low", "Volume"]])
        DI_minus = stocks['mdi']
        DI_plus = stocks['pdi']
        data = DI_plus.subtract(DI_minus)
        self.data = data
        return data


class Stochastic(Indicator):
    def __init__(self, data, period, color='#000000'):
        super().__init__('Stochastic-' + str(period), color)
        self.period = period
        self.data = self.evaluate(data)
    
    def evaluate(self, stockDF):    
        stocks = StockDataFrame.retype(
            stockDF[["Open", "Close", "High", "Low", "Volume"]])
        stocks.KDJ_WINDOW = self.period
        self.data = stocks['kdjd']
        return stocks['kdjd']
        
        
class DMI_Stochastic(Indicator):
    ### DMI stochastic with a 3 period for High and Low and 3 period for average ###
    def __init__(self, stockDF, color='#000000', period=10):
        super().__init__('DMI Stochastic', color)
        self.period = period
        self.DMIS_K = None
        self.DMI = None
        self.data = self.evaluate(stockDF)
    
    def evaluate(self, stockDF):    
        DMI_Indicator = DMI(stockDF)
        DMI_data = DMI_Indicator.data
        
        DMIS= pd.DataFrame(index = DMI_data.index)
        DMIS['DMIS_K'] = 0
        DMIS['DMIS_D'] = 0
        
        HL_period = 3
        # HL_period = self.period
        
        for i in range(DMI_data.shape[0]):
            if i >= HL_period:
                
                Period_data = DMI_data[i - HL_period + 1 : i + 1]
                
                High = max(Period_data)
                Low = min(Period_data)
                DMI_value = DMI_data[i]
                
                DMIS['DMIS_K'].iloc[i] = 100 * (DMI_value - Low) / (High - Low)
                
            # if i >= 2*self.period:
            DMIS['DMIS_D'] = DMIS['DMIS_K'].rolling(3).mean()
        
        self.data = DMIS['DMIS_D']
        self.DMIS_K = DMIS['DMIS_K']
        self.DMI = DMI_data
        
        return DMIS['DMIS_D']