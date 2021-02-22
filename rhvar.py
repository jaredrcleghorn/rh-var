import json
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

for position in robinhood.get_positions():
    print(f"{position['symbol']} ({position['quantity']})")

print()
