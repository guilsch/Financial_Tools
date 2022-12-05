from turtle import width
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as md
import numpy as np
import pandas as pd

from indicators import Indicator

colors = {'red': '#ff207c',
          'grey': '#42535b',
          'blue': '#207cff',
          'orange': '#ffa320',
          'green': '#00ec8b',
          'black': '#000000',
          'macd' : '#ff6600',
          'macds' : '#edc453',
          'macdh' : '#00ec8b',
          'DMI' : '#027899',
          'DMI_Stoch' : '#207cff',
          'RSI' : '#00ee22'
          }

config_ticks = {'size': 14, 'color': colors['grey'], 'labelcolor': colors['grey']}
config_title = {'size': 18, 'color': colors['grey'], 'ha': 'left', 'va': 'baseline'}

def createSubplots(showVol, inChart2, inChart3):
    subplots_nb = 1
    
    if showVol:
        subplots_nb += 1
    
    if inChart2 is not None:
        subplots_nb += 1
        
    if inChart3 is not None:
        subplots_nb += 1
    
    return [plt.subplots(subplots_nb, 1), subplots_nb]


def getCharts(stockData, inChart1 = None, inChart2 = None, inChart3 = None, buySignals = None, sellSignals = None, showVolume = False):
    
    ### Create figure ###
    
    [fig, axes] , nb_plots = createSubplots(showVolume, inChart2, inChart3)    
    subplot_nb = 1
    
    ### Price chart ###
    
    # Create chart 1
    price_chart = axes
    if nb_plots > 1:
        price_chart = axes[0]
    
    price_chart.set_ylabel('')
    price_chart.grid(axis='both', color='gainsboro', linestyle='-', linewidth=0.5)
    # price_chart.grid(which='minor', alpha=0.2)
    # price_chart.grid(which='major', alpha=0.5)
    
    
    # Plot prices
    price_chart.plot(stockData[['Close']], color=colors['black'], linewidth=1.5, label='Close')
    
    # Plot other indicators
    if inChart1 is not None:
        for indicator in inChart1:
            if isinstance(indicator, Indicator):
                if indicator.inLegend:
                    price_chart.plot(indicator.data, color=indicator.color, linewidth=1, label=indicator.name)
                else:
                    price_chart.plot(indicator.data, color=indicator.color, linewidth=1)
            elif isinstance(indicator, pd.Series):
                price_chart.plot(indicator, linewidth=1, label=indicator.name)
    
    # Add legend
    plot_legend = price_chart.legend(loc='upper left', bbox_to_anchor=(-0.005, 0.95), fontsize=16)
    
    # Plot buy signals
    if buySignals is not None:
        for time in stockData.index:
            if buySignals.data['Signal'][time] == 1:
                price_chart.plot(md.date2num(time), stockData['Close'][time], marker="o", markersize=5, markerfacecolor="green", markeredgecolor="green")
                
    # Plot sell signal            
    if sellSignals is not None:
        for time in stockData.index:
            if sellSignals.data['Signal'][time] == 1:
                price_chart.plot(md.date2num(time), stockData['Close'][time], marker="o", markersize=5, markerfacecolor="red", markeredgecolor="red")
    
    
    ### Volume chart ###
    
    if showVolume:
        volume_chart = axes[subplot_nb]
        volume_chart.set_ylabel('Volume')
        volume_chart.grid(axis='both', color='gainsboro', linestyle='-', linewidth=0.5)
        volume_chart.plot(stockData[['Volume']], color=colors['grey'], linewidth=1, label='Volume')
        subplot_nb += 1
    
    
    ### Chart 2 ###
    
    if inChart2 is not None:
        
        chart2 = axes[subplot_nb]
        chart2.set_ylabel('Indicators')
        chart2.grid(axis='both', color='gainsboro', linestyle='-', linewidth=0.5)
        
        for indicator in inChart2:
            if isinstance(indicator, Indicator):
                if indicator.inLegend:
                    chart2.plot(indicator.data, color=indicator.color, linewidth=1, label=indicator.name)
                else:
                    chart2.plot(indicator.data, color=indicator.color, linewidth=1)
            elif isinstance(indicator, pd.Series):
                chart2.plot(indicator, linewidth=1, label=indicator.name)
        
        chart2.legend(loc='upper left', bbox_to_anchor=(-0.005, 0.95), fontsize=16)
        subplot_nb += 1
        
        
    ### Indicators chart 3 ###
    
    if inChart3 is not None:
        
        chart3 = axes[subplot_nb]
        chart3.set_ylabel('Indicators')
        chart3.grid(axis='both', color='gainsboro', linestyle='-', linewidth=0.5)
        
        for indicator in inChart3:
            if isinstance(indicator, Indicator):
                if indicator.inLegend:
                    chart3.plot(indicator.data, color=indicator.color, linewidth=1, label=indicator.name)
                else:
                    chart3.plot(indicator.data, color=indicator.color, linewidth=1)
            elif isinstance(indicator, pd.Series):
                chart3.plot(indicator, linewidth=1, label=indicator.name)
        
        chart3.legend(loc='upper left', bbox_to_anchor=(-0.005, 0.95), fontsize=16)
        subplot_nb += 1
    
    plt.show()
    
def getResult(stockData, Buy, Sell, minStock = -500, maxStock = 500, initStock = 0, initMoney = 0, stockNB = 1, commission = 0):
    
    stockData_df = stockData
    buy_df = Buy.data
    sell_df = Sell.data
    
    money = initMoney
    money_noFees = initMoney
    stock = initStock
    result_list = []
    time_index = []
    
    for time in stockData_df.index :
        
        if buy_df['Signal'][time] == 1 and stock + 1 <= maxStock:
            price = stockData_df['Close'][time]
            money -= price * stockNB * (1 + commission)
            money_noFees -= price * stockNB
            stock += stockNB
            total = money + stock * price
            total_noFees = money_noFees + stock * price
            result_list.append(['buy', price, stock, money, total, total_noFees])
            time_index.append(time)
            
        if sell_df['Signal'][time] == 1 and stock - 1 >= minStock:
            price = stockData_df['Close'][time]
            money += price * stockNB * (1 - commission)
            money_noFees += price * stockNB
            stock -= stockNB
            total = money + stock * price
            total_noFees = money_noFees + stock * price
            result_list.append(['sell', price, stock, money, total, total_noFees])
            time_index.append(time)
    
    result_df = pd.DataFrame (result_list, columns = ['Type', 'Price', 'Stocks number', 'Money', 'Total', 'Total no fees'], index = time_index)
    
    print(result_df)
    
    return result_df

def getManualResult(stockData, BuyDates, BuyNb, SellDates, SellNb, initStock = 0, initMoney = 0, stockNB = 1, commission = 0):
    
    stockData_df = stockData
    buy_df = Buy.data
    sell_df = Sell.data
    
    money = initMoney
    money_noFees = initMoney
    stock = initStock
    result_list = []
    time_index = []
    
    for time in stockData_df.index :
        
        if buy_df['Signal'][time] == 1 and stock + 1 <= maxStock:
            price = stockData_df['Close'][time]
            money -= price * stockNB * (1 + commission)
            money_noFees -= price * stockNB
            stock += stockNB
            total = money + stock * price
            total_noFees = money_noFees + stock * price
            result_list.append(['buy', price, stock, money, total, total_noFees])
            time_index.append(time)
            
        if sell_df['Signal'][time] == 1 and stock - 1 >= minStock:
            price = stockData_df['Close'][time]
            money += price * stockNB * (1 - commission)
            money_noFees += price * stockNB
            stock -= stockNB
            total = money + stock * price
            total_noFees = money_noFees + stock * price
            result_list.append(['sell', price, stock, money, total, total_noFees])
            time_index.append(time)
    
    result_df = pd.DataFrame (result_list, columns = ['Type', 'Price', 'Stocks number', 'Money', 'Total', 'Total no fees'], index = time_index)
    
    print(result_df)
    
    return result_df

def getDfFromAny(dfOrIndicator):
    
    if isinstance(dfOrIndicator, pd.DataFrame) or isinstance(dfOrIndicator, pd.Series):
        return dfOrIndicator.squeeze()
    
    elif isinstance(dfOrIndicator, Indicator):
        return dfOrIndicator.data.squeeze()