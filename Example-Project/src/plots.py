import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import *
import seaborn as sns
import statsmodels.api as sm

sns.set_style("whitegrid", {'axes.edgecolor': '.6', 
                            'axes.facecolor': '0.9', 
                            'grid.color': '.82', 
                            'legend.frameon': True,
                            'axes.labelsize': 'small'})

def get_lagged_series(series, order=1, log=False):
    lagged = None
    if log:
        lagged = np.log(series).diff(order).dropna();
    else:
        lagged = series.diff(order).dropna();
    
    return lagged

def plot_stocks(index, stocks, labels, positions=None, label_annually=True):
    """
    Plots up to 5 stocks
    
    Args:
        index (DateTimeIndex): date range
        stocks (list): list of stocks to plot
        labels (list): labels to use for plotting
        positions (list of dicts): optional postions to overplot
        label_annually (boolean): plots x label monthly if false, annually otherwise
        
    Returns (None): Will output plot inline
    """
    colors = ['firebrick','steelblue','orange','mediumorchid', 'mediumseagreen']
    
    fig, ax = plt.subplots(figsize=(20,8));
    
    if label_annually:
        span = YearLocator();
        my_format = DateFormatter('%Y');
    else:
        span = MonthLocator();
        my_format = DateFormatter('%b %Y');    
    
    ax.xaxis.set_major_locator(span);
    ax.xaxis.set_major_formatter(my_format);
    ax.autoscale_view();
    
    plt.title('Adjusted Close Prices', fontsize=20);
    plt.ylabel('Adj. Close', fontsize=15);
    plt.xlabel('Time', fontsize=15);
    
    for stock, label, color in zip(stocks, labels, colors):
        ax.plot_date(index, stock, color=color, linestyle='-', marker=None, label=label);
        plt.xticks(rotation=45)
    
    if positions:
        for position in positions:
            ax.axvline(df.index[position['open']], color='lime', linestyle='-')
            ax.axvline(df.index[position['close']], color='red', linestyle='-')
 
    plt.legend(loc=2, prop={'size':15}, frameon=True);

def plot_lagged_series(series, order=1, log=False):
    """
    Plots lagged series
    
    Args: series (ndarray)---time series
          order (int)--------the order of the difference
          log (boolean)------whether to log transform before difference
    Returns: (None) plots inline
    """
    plt.figure(figsize=(12,4));
    plt.xlabel('Time Index');
    plt.ylabel('Difference');
    
    if log:
        plt.title('Log Series Lagged by ' + str(order));
        lagged = get_lagged_series(series, order, log)
    else:
        plt.title('Series Lagged by ' + str(order));
        lagged = get_lagged_series(series, order, log)
        
    plt.plot(np.arange(0,lagged.size,1), lagged);

def plot_correlograms(series, limit=20):
    """
    Plots autocorrelations
    
    Args: series (ndarray)---the time series to view plots for
          limit (ndarry)-----the number of lags to see
    Returns: (None) plots inplace
    """
    
    fig = plt.figure(figsize=(15,8));
    fig.subplots_adjust(hspace=.5)
    ax1 = fig.add_subplot(211);
    fig = sm.graphics.tsa.plot_acf(series, lags=limit, ax=ax1);
    plt.title('Correlogram');
    plt.xticks(np.arange(0,limit+1,1))
    plt.xlim([-1,limit])
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    
    ax2 = fig.add_subplot(212);
    fig = sm.graphics.tsa.plot_pacf(series, lags=limit, ax=ax2);
    plt.title('Partial Correlogram');
    plt.xticks(np.arange(0,limit+1,1))
    plt.xlim([-1,limit])
    plt.xlabel('Lag')
    plt.ylabel('Partial Autocorrelation')
    
def plot_pair(series1, series2, names):
    """
    Plot pair series with name subsitutions
    
    Args: series1 (ndarray)---first stock of the pair
          series2 (ndarray)---second stock of the pair
          names (list)--------list of names for the stocks
    Returns: (None) plots inline
    """
    
    fig, ax = plt.subplots(figsize=(20,8));
    years = YearLocator();
    yearsFmt = DateFormatter('%Y');
    
    ax.xaxis.set_major_locator(years);
    ax.xaxis.set_major_formatter(yearsFmt);
    ax.autoscale_view();
    
    index = series1.index
    
    plt.title(names[0] + ' and ' + 
              names[1] +' (Adj. Close)', fontsize=20);
    plt.ylabel('Adj. Close', fontsize=15);
    plt.xlabel('Time', fontsize=15);
    
    ax.plot_date(index, series1, 'indianred', label=names[0]);
    ax.plot_date(index, series2, 'steelblue', label=names[1]);
 
    plt.legend(loc=2, prop={'size':15}, frameon=True);
    
def plot_ratio(ratio, name, deviations=[1], positions=[]):
    """
    Plots the ratio of the stocks
    
    Args: ratio (ndarray)----the ratio of the stocks in question
          name (string)------the name of the ratio
          devations (list)---the devations to plot
          positions (list)---the positions to plot
    Returns: (None) plots inplace
    """
    fig = plt.subplots(figsize=(20,8));

    plt.title('Ratio ' + name + ' Adjusted Close', fontsize=20);
    plt.ylabel('Ratio', fontsize=15);
    plt.xlabel('Time Index', fontsize=15);
    plt.xlim([0,ratio.size])
    plt.xticks(np.arange(0, ratio.size, 500))
    
    plt.plot(np.arange(ratio.size), ratio, 'black', label='$Ratio$', alpha=0.5);
    plt.plot([0, ratio.size], [ratio.mean(), ratio.mean()], 'steelblue', lw=2, label=r'$\hat{\mu}$');
    
    for color, std in zip(['y','orange','salmon','red'], deviations):
        latex_prep = '$' + str(std) + '$'
        plt.plot([0, ratio.size], [ratio.mean()-std*ratio.std(), ratio.mean()-std*ratio.std()], 
                 '--', lw=2, label='$\hat{\mu} \pm$' + latex_prep + '$\hat{\sigma}$', color=color);
        plt.plot([0, ratio.size], [ratio.mean()+std*ratio.std(), ratio.mean()+std*ratio.std()], 
                 '--', lw=2, color=color);
    
    if positions:
        opening_days, closing_days = [], []
        opening_ratios, closing_ratios = [], []
        
        for position in positions:
            if 'open' in position.keys():
                for day in position['open']:
                    opening_days.append(day)
                    opening_ratios.append(ratio.ix[day])
            if 'close' in position.keys():
                closing_days.append(position['close'])
                closing_ratios.append(ratio.ix[position['close']])
            
        plt.scatter(x=opening_days, y=opening_ratios, s=125, color='lime', edgecolor='black', label='$Open$ '+'$Position$')
        plt.scatter(x=closing_days, y=closing_ratios, s=125, color='red', edgecolor='black', label='$Close$ '+'$Position$')
    
    plt.legend(loc='best', prop={'size':15}, frameon=True);

