import random
from random import randint

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

for i in range(1, num_entries + 1):
    service_loc_id = randint(1, 40)
    device_type = random.choice(device_types)
    model_number = random.choice(device_models[device_type])
    
    mysql_statement = f"INSERT INTO Devices (deviceID, serviceLocID, deviceType, modelNumber) VALUES ({i}, {service_loc_id}, '{device_type}', '{model_number}');"
    mysql_statements.append(mysql_statement)

# Print the generated MySQL statements
for statement in mysql_statements:
    print(statement)
