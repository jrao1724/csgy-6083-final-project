import random
from random import randint
from datetime import datetime as dt
import pandas as pd

device_data = pd.read_csv('./csvs/device_data.csv')
price_data = pd.read_csv('./csvs/energy_prices.csv')
price_data['timePeriodStart'] = pd.to_datetime(price_data['timePeriodStart'])
price_data['timePeriodEnd'] = pd.to_datetime(price_data['timePeriodEnd'])

def generate_timestamp():
    timestamp = dt.timestamp(dt(2022, 8, 1))
    while True:
        timestamp += 60*60
        yield timestamp


generator = generate_timestamp()


# Define device types and their corresponding actions
device_types = ['AC', 'Fridge', 'Lights', 'Washer', 'Dryer', 'Microwave']
device_actions = {
    'AC': ['temp lowered', 'temp raised'],
    'Fridge': ['door opened', 'door closed'],
    'Lights': ['turned on', 'turned off'],
    'Washer': ['quick wash', 'normal', 'ultra'],
    'Dryer': ['quick dry', 'normal', 'ultra'],
    'Microwave': ['low', 'medium', 'high']
}

# Generate MySQL statements
mysql_statements = []

for i in range(801):
    timestamp = dt.fromtimestamp(next(generator))
    priceTimeID = 0
    for index, row in price_data.iterrows():
        if timestamp.time() >= row['timePeriodStart'].time() and timestamp.time() <= row['timePeriodEnd'].time():
            priceTimeID = row['priceTimeID']
            break
    device_type = random.choice(device_types)
    device_action = random.choice(device_actions[device_type])

    if device_type == 'AC':
        totalEnergyConsumed = 5
        eventLabel = device_action
        numValue = random.randint(70, 80)
        deviceID = device_data.loc[device_data['deviceType'] == device_type].sample(n=1)['deviceID'].values[0]
    elif device_type == 'Lights':
        totalEnergyConsumed = 0 if device_action == 'turned off' else 2
        eventLabel = device_action
        numValue = None
        deviceID = device_data.loc[device_data['deviceType'] == device_type].sample(n=1)['deviceID'].values[0]
    elif device_type == 'Fridge':
        totalEnergyConsumed = 0 if device_action == 'door closed' else 4
        eventLabel = device_action
        numValue = None
        deviceID = device_data.loc[device_data['deviceType'] == device_type].sample(n=1)['deviceID'].values[0]
    elif device_type == 'Washer':
        if device_action == 'quick wash':
            totalEnergyConsumed = 4
        elif device_action == 'normal':
            totalEnergyConsumed = 8
        else:
            totalEnergyConsumed = 12
        eventLabel = device_action
        numValue = None
        deviceID = device_data.loc[device_data['deviceType'] == device_type].sample(n=1)['deviceID'].values[0]
    elif device_type == 'Dryer':
        if device_action == 'quick dry':
            totalEnergyConsumed = 4
        elif device_action == 'normal':
            totalEnergyConsumed = 8
        else:
            totalEnergyConsumed = 12
        eventLabel = device_action
        numValue = None
        deviceID = device_data.loc[device_data['deviceType'] == device_type].sample(n=1)['deviceID'].values[0]
    elif device_type == 'Microwave':
        if device_action == 'low':
            totalEnergyConsumed = 2
        elif device_action == 'medium':
            totalEnergyConsumed = 4
        else:
            totalEnergyConsumed = 6
        eventLabel = device_action
        numValue = None
        deviceID = device_data.loc[device_data['deviceType'] == device_type].sample(n=1)['deviceID'].values[0]
    
    mysql_statement = f"INSERT INTO EnergyConsumption (eventTimestamp, eventLabel, numValue, totalEnergyConsumed, deviceID, priceTimeID) VALUES ('{timestamp}', '{eventLabel}', '{numValue}', '{totalEnergyConsumed}', {deviceID}, {priceTimeID});".replace('None', 'NULL')
    mysql_statements.append(mysql_statement)


with open('./queries/energy_consumption_inserts.txt', 'w') as f:
    for statement in mysql_statements:
        f.write(statement + '\n')
