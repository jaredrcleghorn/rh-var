def convert_to_returns(prices):
    return tuple((prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices)))
