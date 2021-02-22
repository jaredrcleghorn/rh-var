def convert_to_returns(y):
    return tuple((y[i] - y[i - 1]) / y[i - 1] for i in range(1, len(y)))
