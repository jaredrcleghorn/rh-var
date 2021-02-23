import json
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import robinhood as rh
from scipy.stats import norm
import statistics
import utils

CONFIG_FILENAME = 'config.json'
DEFAULT_FIG_WIDTH = 12.8
DEFAULT_FIG_HEIGHT = 4.8
PLT_NCOLS = 2

with open(CONFIG_FILENAME) as f:
    config = json.load(f)

device_token = config['robinhood']['device_token']
username = config['robinhood']['username']
password = config['robinhood']['password']

if device_token == '':
    device_token = rh.generate_device_token()

    print()
    robinhood = rh.Robinhood(device_token, username, password)

    config['robinhood']['device_token'] = device_token

    with open(CONFIG_FILENAME, 'w') as f:
        json.dump(config, f, indent='\t')
        f.write('\n')
else:
    robinhood = rh.Robinhood(device_token, username, password)

print()
print('Positions:')
print()

positions = robinhood.get_positions()

for i, position in enumerate(positions):
    print(f"{i + 1}. {position['symbol']} ({position['quantity']})")

print()
print('Please enter one of the numbers above, or press enter to use your entire portfolio: ', end='')

try:
    positions = (positions[int(input()) - 1],)
    num_positions = 1
    fig, axs = plt.subplots(ncols=PLT_NCOLS, figsize=(DEFAULT_FIG_WIDTH, DEFAULT_FIG_HEIGHT))
    axs = (axs,)
except:
    num_positions = len(positions)
    fig, axs = plt.subplots(num_positions, PLT_NCOLS, figsize=(DEFAULT_FIG_WIDTH, num_positions * DEFAULT_FIG_HEIGHT), tight_layout=True)

x = np.empty(num_positions)
X = [None] * num_positions

for i, position in enumerate(positions):
    symbol = position['symbol']
    quantity = position['quantity']
    historicals = robinhood.get_historicals(symbol)

    ax1, ax2 = axs[i]

    dates = tuple(historical['begins_at'] for historical in historicals)
    prices = tuple(historical['close_price'] for historical in historicals)

    ax1.set_title(f'{symbol} Price')
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Price')
    ax1.set_xticks(np.linspace(0, len(historicals) - 1, 5))
    ax1.plot(dates, prices)

    returns = utils.convert_to_returns(prices)

    ax2.set_title(f'{symbol} Return Frequency')
    ax2.set_xlabel('Return')
    ax2.set_ylabel('Frequency')
    ax2.xaxis.set_major_formatter(FuncFormatter(lambda r, pos: f'{round(r * 100)}%'))
    ax2.hist(returns, density=True, rwidth=0.5)

    mean = statistics.mean(returns)
    stdev = statistics.stdev(returns, mean)

    print()
    print(f'{symbol} return stats:')
    print()
    print(f'mean = {round(mean * 100, 4)}%')
    print(f'standard deviation = {round(stdev * 100, 4)}%')

    y = np.linspace(*ax2.get_xlim(), 100)

    ax2.plot(y, norm.pdf(y, mean, stdev))

    x[i] = quantity * prices[-1]
    X[i] = returns

plt.show()

x_sum = np.sum(x)
x = x / x_sum
Sigma = np.cov(X)
sigma = math.sqrt(np.dot(np.dot(x, Sigma), x.transpose()))
var = 2.33 * sigma

print()
print(f"\033[1mEstimated VaR\033[0m: {round(var * 100, 4)}% or ${round(var * x_sum)}")
print()
