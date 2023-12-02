import random
from random import randint
import pandas as pd
import datetime as dt

mysql_statements = []

time_period_list = []
for i in range(0, 12):
    for k in range(10001, 10021):
        time_period_dict = {
            "priceTimeID": i+1,
            "timePeriodStart": str(dt.timedelta(hours=i*2)),
            "timePeriodEnd": str(dt.timedelta(hours=(i*2 + 2))).replace('1 day, ', ''),
            "zipCode": str(k),
            "price": randint(1, 5)
        }
        time_period_list.append(time_period_dict)

        mysql_statement = f"""INSERT INTO EnergyPrices (priceTimeID, zipCode, timePeriodStart, timePeriodEnd, price) VALUES ({time_period_dict["priceTimeID"]}, '{time_period_dict["zipCode"]}', '{time_period_dict["timePeriodStart"]}','{time_period_dict["timePeriodEnd"]}', '{time_period_dict["price"]}');"""

        # print(mysql_statement)
        mysql_statements.append(mysql_statement)

df = pd.DataFrame(time_period_list)

df.to_csv('./csvs/energy_prices.csv')

with open('./queries/price_time_data_inserts.txt', 'w') as f:
    for stmt in mysql_statements:
        f.write(stmt + '\n')


