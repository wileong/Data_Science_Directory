import numpy as np
import pandas as pd
import Quandl

def get_adj_close(tickers, start, end="", ratios=[], log_transforms=[]):
    """
    Args:
        tickers (list): collection of ticker symbols for which to collect adj. close 
                daily prices for
        start (string, format: 2013-01-01): start date for which to collect prices after
        end (string, format: 2013-01-01): optional end date, today if not specified
        ratios (list): collection of tuples of tickers from 'tickers' list to calculate 
                price ratios for (the stock with larger mean is numerator)
        log_transforms (list): collection of tickers from 'tickers' to include additional 
                natural log transformed copies
    
    Returns (dataframe): all adj. close prices, ratios, and log transforms specified
    """ 
    result = {}
    
    for ticker in tickers:
        try:
            result[ticker] = Quandl.get('WIKI/'+ticker, trim_start=start, trim_end=end)['Adj. Close']
        except DatasetNotFound:
            print('ERROR:', ticker, 'is not a vaild ticker')
        except ErrorDownloading:
            print('ERROR: API Limit reached')

    for ratio in ratios:
        try:
            ticker1, ticker2 = ratio
            if result[ticker1].mean() > result[ticker2].mean():
                result[ticker1+'/'+ticker2] = result[ticker1]/result[ticker2]
            else:
                result[ticker2+'/'+ticker1] = result[ticker2]/result[ticker1]
        except KeyError:
            print('ERROR:', ticker1, 'or', ticker2, 'are not in the list of specified tickers')
    
    for log_transform in log_transforms:
        try:
            result['ln('+log_transform+')'] = np.log(result[log_transform])
        except KeyError:
            print('ERROR:', log_transform, 'is not in the list of specified tickers')
    
    return pd.DataFrame(result).dropna() # drop na here because of differences in lenght of history for stocks
