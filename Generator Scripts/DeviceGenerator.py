import random
from random import randint
import pandas as pd

# Define device types and their corresponding models
device_types = ['AC', 'Fridge', 'Lights', 'Washer', 'Dryer', 'Microwave']
device_models = {
    'AC': ['CoolMax-X1', 'CoolBreeze-3000'],
    'Fridge': ['FrostFree-200', 'ChillMaster-500'],
    'Lights': ['LED-BrightLite', 'SmartGlow-200'],
    'Washer': ['EcoClean-500', 'TurboWash-1000'],
    'Dryer': ['QuickDry-700', 'UltraDry-800'],
    'Microwave': ['HeatWave-900', 'SmartCook-1200']
}

# Generate MySQL statements
num_entries = 80
mysql_statements = []
device_data_list = []

for i in range(1, num_entries + 1):
    service_loc_id = randint(1, 40)
    device_type = random.choice(device_types)
    model_number = random.choice(device_models[device_type])
    
    device_data_list.append({
        "deviceID": i,
        "serviceLocID": service_loc_id,
        "deviceType": device_type,
        "modelNumber": model_number
    })

    mysql_statement = f"INSERT INTO Devices (deviceID, serviceLocID, deviceType, modelNumber) VALUES ({i}, {service_loc_id}, '{device_type}', '{model_number}');"
    mysql_statements.append(mysql_statement)

# Print the generated MySQL statements
for statement in mysql_statements:
    print(statement)

df = pd.DataFrame(device_data_list)

df.to_csv('./csvs/device_data.csv')

with open('./queries/device_data_inserts.txt', 'w') as f:
    for stmt in mysql_statements:
        f.write(stmt + '\n')

