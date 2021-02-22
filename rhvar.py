import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import robinhood as rh
import utils

CONFIG_FILENAME = 'config.json'

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
print('Please enter one of the numbers above: ', end='')

symbol = positions[int(input()) - 1]['symbol']
historicals = robinhood.get_historicals(symbol)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12.8, 4.8))

x = tuple(historical['begins_at'] for historical in historicals)
y = tuple(historical['close_price'] for historical in historicals)

ax1.set_title(f'{symbol} Price')
ax1.set_xlabel('Day')
ax1.set_ylabel('Price')
ax1.set_xticks(np.linspace(0, len(historicals) - 1, 5))
ax1.plot(x, y)

y = utils.convert_to_returns(y)

ax2.set_title(f'{symbol} Return Frequency')
ax2.set_xlabel('Return')
ax2.set_ylabel('Frequency')
ax2.xaxis.set_major_formatter(FuncFormatter(lambda r, pos: f'{round(r * 100)}%'))
ax2.hist(y, rwidth=0.5)

plt.show()

print()
