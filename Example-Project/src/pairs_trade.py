from random_walk_forcast import *

def identify_positions(ratio, k, start=50):
    """
    Identifies all positions using a dynamic step value
    
    Args: ratio (ndarray)---the ratio of the stocks
          k (int)-----------the intial devation to open a position
          start (int)-------the day to start
    Results: (list of maps) the positions
    """
    results = []
    result = {"open":[]}
    mean, sd = ratio.mean(), ratio.std()
    day, size = start, ratio.size
    
    while day < size:   
        if abs(ratio.ix[day] - mean) > k*sd:
            result["open"].append(day)
            walk = get_expected_walk(ratio[:day], 20)[1]
            day += int(walk.max() / walk.min())
        elif abs(ratio.ix[day] - mean) < 0.05 and len(result["open"]) > 0 :
            result["close"] = day
            results.append(result)
            result = {"open":[]}
            day += 1
        else:
            day += 1
            
    if len(result['open']) > 0:
        result['close'] = day-1
        results.append(result)
        
    return results

def back_trade(init_investment, numer_prices, denom_prices, ratio, positions, swap_count=50):

    """
    Back trades with the given positions
    
    Args: init_investment (int)----initial total investment
          numer_prices (ndarray)---the series of the numerator stock w/ respect to the ratio
          denom_prices (ndarry)----the series of the denominator stock w/ respect to the ratio
          ratio (ndarray)----------the ratio of the series'
          positions (list of maps)-the postions to trade on
          swap_count (int)---------the number of stocks to swap at a given open position
    Returns: (map) the result object
    """
    cur_portfolio_value = init_investment
    
    
    for position in positions:
        if all(ratio[position['open']] > ratio.mean()):
            openings = len(position['open'])
            cur_portfolio_value += np.sum(swap_count*numer_prices[position['open']])
            cur_portfolio_value -= np.sum(swap_count*denom_prices[position['open']])

            cur_portfolio_value -= openings*swap_count*numer_prices[position['close']]
            cur_portfolio_value += openings*swap_count*denom_prices[position['close']]
        elif all(ratio[position['open']] < ratio.mean()):
            openings = len(position['open'])
            cur_portfolio_value -= np.sum(swap_count*numer_prices[position['open']])
            cur_portfolio_value += np.sum(swap_count*denom_prices[position['open']])

            cur_portfolio_value += openings*swap_count*numer_prices[position['close']]
            cur_portfolio_value -= openings*swap_count*denom_prices[position['close']]
    
    return {'init_investment': init_investment,
            'net_gain': cur_portfolio_value - init_investment,
            'net_gain/year': (cur_portfolio_value - init_investment) / (len(ratio) / 252) } # 252 trade days / year