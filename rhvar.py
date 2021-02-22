import json
import matplotlib.pyplot as plt
import numpy as np
import robinhood as rh

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
x = tuple(historical['begins_at'] for historical in historicals)
y = tuple(historical['close_price'] for historical in historicals)

plt.title(symbol)
plt.xlabel('Day')
plt.ylabel('Price')
plt.xticks(np.linspace(0, len(historicals) - 1, 5))
plt.plot(x, y)
plt.show()

print()
