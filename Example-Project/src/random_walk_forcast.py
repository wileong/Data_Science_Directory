import pandas as pd
import numpy as np
from plots import *
import scipy.optimize as opt

def neg_log_llh(theta, data):
    """
    Args theta (list)-----the params [mu, sigma**2]
         data (ndarray)---data points to be fit by log normal distribution
        
    Return (double): negative log-likelihood for the log normal.
    """
    
    mu, sigma = theta[0], np.sqrt(theta[1])
    neg_log_llhs = np.log(data*sigma*np.sqrt(2*np.pi)) + ((np.log(data)-mu)**2/(2*(sigma**2))) 
    
    return neg_log_llhs.sum()

def mle_log_norm(data, init_theta=[1,1]):
    """
    Args: theta (list)-----the params [mu, sigma**2]
          data (ndarray)---data points to be fit by log normal distribution
    
    Return (list): mu, sigma**2 for fitted log normal params
    """
    
    fit = opt.minimize(neg_log_llh, init_theta, data, method='Nelder-Mead')
    return fit.x

def get_daily_return_ratio(series):
    """
    Args: series (ndarray)----the time series to get the lagged return ratios
          window_size (int)---number of trading weeks to use
    Return: (ndarray) y(t)/y(t-1) over the weeks specified
    """

    return (series[1:]/series[:-1])

def simulate_random_walk(series, window_size=10, ahead=50):
    """
    Args: series (ndarray)----time series to use
          window_size (int)---number of trading weeks to use for log normal estimation
          ahead (int)---------how many days do you want to forcast head for
    
    Return (ndarray): simulated future price
    """
    
    forcasts = np.zeros(ahead)
    window = series[-((window_size*5)+1):].values

    for step in range(ahead):
        mu, sigma2 = mle_log_norm( get_daily_return_ratio(window) )
        forcast = window[-1]*np.random.lognormal(mu, np.sqrt(sigma2), 1)
        forcasts[step] = forcast
        window = np.roll(window, -1)
        window[-1] = forcast
    
    return forcasts

def get_expected_walk(series, window_size=10, ahead=50):
    """
    Args: series (ndarray)----time series to use
          window_size (int)---number of trading weeks to use for log normal estimation
          ahead (int)---------how many days do you want to forcast head for
    
    Return (ndarray): simulated future price
    """
    E_Xs = np.zeros(ahead)
    V_Xs = np.zeros(ahead)
    yt = series[-1]
    last_price = series[-1]
    window = series[-((window_size*5)+1):].values

    for step in range(ahead):
        mu, sigma2 = mle_log_norm( get_daily_return_ratio(window) )
        E_Xs[step] = last_price * get_expected_value(mu, sigma2)
        V_Xs[step] = get_k_step_variance(mu, sigma2, step+1, yt)
        last_price = last_price * get_expected_value(mu, sigma2)
        
    return E_Xs, V_Xs

def get_expected_value(mu, sigma2):
    """
    Returns expected value for log normal with params mu, sigma2
    
    Args: mu (float)-------parameter mu
          sigma2 (float)---parameter sigma squared
    
    Returns: expected value (float) of the log normal
    """
    
    return (np.exp((mu+sigma2)/2))

def get_variance(mu, sigma2):
    """
    Returns variance for log normal with params mu, sigma2
    
    Args: mu (float)-------parameter mu
          sigma2 (float)---parameter sigma squared
    
    Returns: variance (float) of the log normal
    """
    
    return (np.exp(sigma2)-1)*np.exp((2*mu)+sigma2)

def get_k_step_variance(mu, sigma2, k, yt):
    """
    Returns a k step ahead variance for log normal with params mu, sigma2
    
    Args: mu (float)-------parameter mu
          sigma2 (float)---parameter sigma squared
          k (int)----------number of steps ahead
          yt (float)-------price at time t (end of sample)
          
    Returns: variance (float) of the log normal
    """
    
    return (yt**2) * ((get_variance(mu, sigma2) + get_expected_value(mu, sigma2)**2)**k - (get_expected_value(mu, sigma2)**2)**k)

def plot_expected_forcast(series, window, ahead, train_on=None, error=2):
    """
    Plots Expected Forcast and Original Series
    
    Args: series (ndarray)---time series for which to forcast
          window (int)-------window size for MLE of log normal
          ahead (int)--------number of days to forcast for
          train_on (int)-----optional, number of days from series to use to forcast
          error (int)--------number of standard devations to use for confidence bands
          
    Returns: None, plots inline
    """
    
    if not train_on:
        train_on = series.count()
    
    mu, sigma2 = get_expected_walk(series[:train_on], window, ahead)
    low_bound = mu-(error*np.sqrt(sigma2))
    high_bound = mu+(error*np.sqrt(sigma2))
    
    train_x_space = np.arange(0,series.count())
    test_x_space = np.arange(train_on, train_on+ahead)
    
    plt.figure(figsize=(15,6));
    plt.plot(train_x_space, series);
    plt.plot(test_x_space, mu, 'maroon');
    plt.plot(test_x_space, high_bound, 'olive');
    plt.plot(test_x_space, low_bound, 'olive');
    plt.fill_between(test_x_space, low_bound, high_bound, alpha=0.2, color='y')
    
    plt.xlabel('Time Index (Days)');
    plt.ylabel('Adjusted Close Price');
    plt.title('Expected Log Normal Random Walk Forcast');

def plot_simulated_forcast(series, window, ahead, train_on=None, n=10):
    """
    Plots Simulated Forcast and Original Series
    
    Args: series (ndarray)---time series for which to forcast
          window (int)-------window size for MLE of log normal
          ahead (int)--------number of days to forcast for
          train_on (int)-----optional, number of days from series to use to forcast
          n (int)------------number of simulations to plot
    
    Returns: None, plots inline
    """ 

    if not train_on:
        train_on = series.count()
    
    train_x_space = np.arange(0,series.count())
    test_x_space = np.arange(train_on, train_on+ahead)
    
    plt.figure(figsize=(15,6));
    plt.plot(train_x_space, series)
    for _ in range(n):
        walk = simulate_random_walk(series[:train_on], window, ahead)
        plt.plot(test_x_space, walk, linestyle='-', color='pink', alpha=0.8)
    
    plt.xlabel('Time Index (Days)');
    plt.ylabel('Adjusted Close Price');
    plt.title('Simulated Log Normal Random Walk Forcast');
