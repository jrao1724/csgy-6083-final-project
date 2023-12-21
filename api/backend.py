import mysql.connector as sql_connect
from mysql.connector import errorcode
from mysql.connector import (connection)
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin

import pandas as pd
import datetime

app = Flask(__name__)
cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


try:
    sql_connection = connection.MySQLConnection(
        user='root',
        host='127.0.0.1',
        database='final_project_copy'
    )
    cursor = sql_connection.cursor(dictionary=True)
    # query = "select * from EnergyConsumption"
    # cursor.execute(query)
    # records = cursor.fetchall()

    # print(records)



    # # print(records)
    # for record in records:
    #     # print(f"First Name: {record['firstName']}\tLast Name: {record['lastName']}")
    #     print(record)


except sql_connect.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


@app.route('/login', methods=['POST'])
def authenticate_user():
    print(request)
    email = request.form['email']
    password = request.form['password']

    query = ("select * from Customers where email = %s")
    cursor.execute(query, (email,))

    records = cursor.fetchall()
    print(records)

    if records:
        if records[0]['password'] != password:
            response = make_response(
                jsonify(
                    {"message": "Incorrect password."}
                ),
                403
            )
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(
                jsonify(
                    {
                        "message": "Successfully authenticated user!",
                        "email": email,
                        "customerID": records[0]['customerID']
                    }
                ),
                200
            )
            response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
            jsonify(
                {"message": "User does not exist"}
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/registerUser', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['fname']
    last_name = request.form['lname']
    street_addr = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zipcode']

    query = ("select * from Customers where email = %s")
    cursor.execute(query, (email,))

    records = cursor.fetchall()

    if (records):
        response = make_response(
            jsonify(
                {"message": "User already exists."}
            ),
            400
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        last_id_query = ("SELECT customerID FROM Customers ORDER BY customerID DESC LIMIT 1")
        cursor.execute(last_id_query)
        records = cursor.fetchall()

        query = ("""insert into Customers (customerID, firstName, lastName, streetAddress, city, zipCode, state, email, password)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
        try:
            cursor.execute(query, (int(records[0]['customerID']) + 1, first_name, last_name, street_addr, city, zip_code, state, email, password,))
            sql_connection.commit()
            response = make_response(
                jsonify(
                    {
                        "message": "User registered successfully!",
                        "customerID": int(records[0]['customerID']) + 1,
                        "email": email
                    }
                ),
                200
            )
            response.headers["Content-Type"] = "application/json"
            return response
        except Exception as e:
            response = make_response(
                jsonify(
                    {"message": f"Error registering user: {str(e)}"}
                ),
                404
            )
            response.headers["Content-Type"] = "application/json"
            return response


@app.route('/addServiceLocation', methods=['POST'])
def add_new_service_location():
    customerID = request.form['customerID']
    dateTakenOver = request.form['dateTakenOver']
    squareFootage = request.form['squareFootage']
    street_addr = request.form['streetAddr']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zipCode']
    unit = request.form['unit']
    numBedrooms = request.form['numBedrooms']
    numOccupants = request.form['numOccupants']

    query = ("select * from ServiceLocations where \
     streetAddress = %s and city = %s and zipCode = %s and state = %s and unit = %s")
    cursor.execute(query, (street_addr, city, zip_code, state, unit,))
    records = cursor.fetchall()

    if (records):
        response = make_response(
            jsonify(
                {"message": "Service Location already exists."}
            ),
            400
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        last_id_query = ("SELECT serviceLocID FROM ServiceLocations ORDER BY serviceLocID DESC LIMIT 1")
        cursor.execute(last_id_query)
        records = cursor.fetchall()

        query = ("""insert into ServiceLocations (serviceLocID, customerID, dateTakenOver, squareFootage, streetAddress, city, zipCode, state, unit, numBedrooms, numOccupants)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
        try:
            cursor.execute(query, (int(records[0]['serviceLocID']) + 1, customerID, dateTakenOver, squareFootage, street_addr, city, zip_code, state, unit, numBedrooms, numOccupants,))
            sql_connection.commit()
            response = make_response(
                jsonify(
                    {"message": "Service Location added successfully!"}
                ),
                200
            )
            response.headers["Content-Type"] = "application/json"
            return response
        except Exception as e:
            response = make_response(
                jsonify(
                    {"message": f"Error adding serviceLocation: {str(e)}"}
                ),
                404
            )
            response.headers["Content-Type"] = "application/json"
            return response

@app.route('/updateServiceLocation', methods=['POST'])
def update_service_location():
    serviceLocID = request.form['serviceLocID']
    customerID = request.form['customerID']
    dateTakenOver = request.form['dateTakenOver']
    squareFootage = request.form['squareFootage']
    street_addr = request.form['streetAddr']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zipCode']
    unit = request.form['unit']
    numBedrooms = request.form['numBedrooms']
    numOccupants = request.form['numOccupants']

    query = ("select * from ServiceLocations where \
     streetAddress = %s and city = %s and zipCode = %s and state = %s and unit = %s")
    cursor.execute(query, (street_addr, city, zip_code, state, unit,))
    records = cursor.fetchall()

    if (records):
        update_service_loc = ("UPDATE ServiceLocations SET streetAddress = %s and city = %s and zipCode = %s and state = %s and unit = %s and dateTakenOver = %s and squareFootage = %s and numBedrooms = %s and numOccupants = %s WHERE serviceLocID = %s")
        cursor.execute(update_service_loc, (street_addr, city, zip_code, state, unit, dateTakenOver, squareFootage, numBedrooms, numOccupants, serviceLocID,))
        sql_connection.commit()
        
        response = make_response(
            jsonify(
                {"message": "Service Location updated successfully"}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
            jsonify(
                {"message": "Service Location not found. "}
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/deleteServiceLocation', methods=['POST'])
def delete_service_location():
    serviceLocID = request.form['serviceLocID']

    query = ("select * from ServiceLocations where serviceLocID = %s")
    cursor.execute(query, (serviceLocID,))
    records = cursor.fetchall()

    if (records):
        update_service_loc = ("DELETE from ServiceLocations WHERE serviceLocID = %s")
        cursor.execute(update_service_loc, (serviceLocID,))
        sql_connection.commit()
        
        response = make_response(
            jsonify(
                {"message": "Service Location successfully deleted"}
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
            jsonify(
                {"message": "Service Location not found. "}
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/getServiceLocations', methods=['POST'])
def get_service_locations():
    customerID = request.args.get("customerID")

    query = ("select * from ServiceLocations where customerID = %s;")
    cursor.execute(query, (customerID,))

    serviceLocations = cursor.fetchall()
    # print(serviceLocations)

    total_service_loc_data = []

    if (serviceLocations):
        try:
            for sl in serviceLocations:
                print(sl)
                serviceLocID = sl['serviceLocID']

                query = ("select * from Devices where serviceLocID = %s;")
                cursor.execute(query, (serviceLocID,))
                device_records = cursor.fetchall()
                total_price_to_date = 0
                total_devices = 0

                total_devices_by_type = {}

                for device in device_records:
                    deviceID = device['deviceID']

                    query = ("select *, (ec.totalEnergyConsumed * ep.price) as deviceCost from EnergyConsumption ec \
                        join EnergyPrices ep on ec.priceTimeID = ep.priceTimeID \
                        where ec.deviceID = %s \
                        group by ec.eventTimestamp;")
                    cursor.execute(query, (deviceID,))
                    energy_consumption_records = cursor.fetchall()
                    
                    print("ENERGY CONSUMPTION RECORDS")
                    print(energy_consumption_records)

                    cost_for_device = 0

                    for rec in energy_consumption_records:
                        cost_for_device += float(rec['deviceCost'])

                    print(cost_for_device)
                
                    total_price_to_date += cost_for_device
                    total_devices += 1

                    if device['deviceType'] not in total_devices_by_type:
                        total_devices_by_type[device['deviceType']] = 1
                    else:
                        total_devices_by_type[device['deviceType']] += 1

                service_loc_data = {
                    "serviceLocID": sl['serviceLocID'],
                    "streetAddress": sl['streetAddress'],
                    "unit": sl['unit'],
                    "city": sl['city'],
                    "state": sl['state'],
                    "zipCode": sl['zipCode'],
                    "dateTakenOver": sl['dateTakenOver'],
                    "squareFootage": sl['squareFootage'],
                    "numBedrooms": sl['numBedrooms'],
                    "numOccupants": sl['numOccupants'],
                    "totalCost": total_price_to_date,
                    "totalDevices": total_devices,
                    "totalDevicesByType": total_devices_by_type
                }

                print(service_loc_data)

                total_service_loc_data.append(service_loc_data)
    
            response = make_response(
                    jsonify(
                        {
                            'message': f'Successfully retrieved service location data for customer: {customerID}',
                            'allServiceLocData': total_service_loc_data
                        }
                    ),
                    200
                )
            response.headers["Content-Type"] = "application/json"
            return response
        except Exception as e:
            response = make_response(
                jsonify(
                    {"message": f"Error retrieving service locations: {str(e)}"}
                ),
                404
            )
            response.headers["Content-Type"] = "application/json"
            return response


@app.route('/energyUsagePerDay', methods=['POST'])
def get_energy_usage_per_day():
    serviceLocID = request.args.get('serviceLocID')

    query = ("select *, sum(totalEnergyConsumed) as totalPerDay from EnergyConsumption ec \
        join Devices d on d.deviceID = ec.deviceID \
        where d.serviceLocID = %s \
        group by Date(ec.eventTimestamp);")
    
    cursor.execute(query, (int(serviceLocID),))
    records = cursor.fetchall()

    data_dict = {}

    for record in records:
        data_dict[str(datetime.datetime.date(record['eventTimestamp']))] = record['totalPerDay']

    response = make_response(
        jsonify(
            {
                "message": "Retrieved service location usage",
                "dateList": data_dict
            }
        ),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/energyUsagePerWeek', methods=['POST'])
def get_energy_usage_per_week():
    serviceLocID = request.args.get('serviceLocID')

    query = ("select *, sum(totalEnergyConsumed) as totalPerDay from EnergyConsumption ec \
        join Devices d on d.deviceID = ec.deviceID \
        where d.serviceLocID = %s \
        group by Date(ec.eventTimestamp);")
    
    cursor.execute(query, (int(serviceLocID),))
    records = cursor.fetchall()

    data_dict = {}

    for record in records:
        data_dict[str(datetime.datetime.date(record['eventTimestamp']))] = record['totalPerDay']

    date_energy_df = pd.DataFrame(data_dict.items(), columns=['Date', 'Usage'])

    # print(date_energy_df)

    date_energy_df['Usage'] = date_energy_df['Usage'].astype(float)
    date_energy_df['Date'] = pd.to_datetime(date_energy_df['Date'])

    date_energy_df = date_energy_df.resample('W-Mon',on='Date')['Usage'].sum().reset_index()
    date_energy_df.rename(columns={'Date': 'Week'}, inplace=True)
    # print(date_energy_df)
    date_energy_df['Week'] = date_energy_df['Week'].astype(str)
    # print(date_energy_df.set_index('Week').T.to_dict())

    response = make_response(
        jsonify(
            {
                "message": "Retrieved service location usage",
                "weeklyEnergyUsage": date_energy_df.set_index('Week').T.to_dict()
            }
        ),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/energyUsagePerMonth', methods=['POST'])
def get_energy_usage_per_month():
    serviceLocID = request.args.get('serviceLocID')

    query = ("select *, sum(totalEnergyConsumed) as totalPerMonth from EnergyConsumption ec \
        join Devices d on d.deviceID = ec.deviceID \
        where d.serviceLocID = %s \
        group by Month(ec.eventTimestamp);")
    
    cursor.execute(query, (int(serviceLocID),))
    records = cursor.fetchall()

    data_dict = {}

    for record in records:
        data_dict[str(datetime.datetime.date(record['eventTimestamp']))] = record['totalPerMonth']

    response = make_response(
        jsonify(
            {
                "message": "Retrieved service location usage per month",
                "dateList": data_dict
            }
        ),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getDevices', methods=['POST'])
def get_devices():
    serviceLocID = request.args.get('serviceLocID')

    query = ("select * from Devices where serviceLocID = %s;")

    cursor.execute(query, (serviceLocID,))
    records = cursor.fetchall()

    if records:
        response = make_response(
            jsonify(
                {
                    "message": f"Retrieved devices for serviceLocID: {serviceLocID}",
                    "data": records 
                }
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(
            jsonify(
                {
                    "message": "No devices in this service location."
                }
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/addDevice', methods=['POST'])
def add_devices():
    serviceLocID = request.form['serviceLocID']
    deviceType = request.form['deviceType']
    deviceModel = request.form['deviceModel']

    try:
        last_id_query = ("SELECT deviceID FROM Devices ORDER BY deviceID DESC LIMIT 1")
        cursor.execute(last_id_query)
        last_id = cursor.fetchall()

        print(int(last_id[0]['deviceID']) + 1)
    
        query = ("insert into Devices (deviceID, serviceLocID, deviceType, modelNumber) \
        values (%s, %s, %s, %s)")

        cursor.execute(query, (str(int(last_id[0]['deviceID']) + 1), serviceLocID, deviceType, deviceModel,))
        sql_connection.commit()
        response = make_response(
            jsonify(
                {
                    "message": f"Successfully added device to {serviceLocID}",
                }
            ),
            200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
        response = make_response(
            jsonify(
                {
                    "message": f"Could not add device to this serviceLocID. Error: {str(e)}"
                }
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/updateDeviceInfo', methods=['POST'])
def update_device_info():
    deviceID = request.form['deviceID']
    serviceLocID = request.form['serviceLocID']
    deviceType = request.form['deviceType']
    deviceModel = request.form['deviceModel']

    try:
        check_for_device = ("SELECT * from Devices where deviceID = %s")
        cursor.execute(check_for_device, (deviceID,))
        device_exists = cursor.fetchall()

        if (device_exists):
            update_device = ("UPDATE Devices SET deviceType = %s, deviceModel = %s WHERE deviceID = %s;")
            cursor.execute(update_device, (deviceType, deviceModel, deviceID,))
            sql_connection.commit()

            response = make_response(
                jsonify(
                    {
                        "message": f"Successfully updated device information for deviceID: {deviceID}"
                    }
                ),
                200
            )
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(
                jsonify(
                    {
                        "message": "The requested device does not exist."
                    }
                ),
                404
            )
            response.headers["Content-Type"] = "application/json"
            return response
    except Exception as e:
        response = make_response(
            jsonify(
                {
                    "message": f"Error occurred while checking for devices: {str(e)}"
                }
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/deleteDevice', methods=['POST'])
def delete_device():
    deviceID = request.form['deviceID']

    try:
        check_for_device = ("SELECT * from Devices where deviceID = %s")
        cursor.execute(check_for_device, (deviceID,))
        device_exists = cursor.fetchall()

        if (device_exists):
            delete_device = ("DELETE from Devices where deviceID = %s")
            cursor.execute(delete_device, (deviceID,))
            sql_connection.commit()

            response = make_response(
                jsonify(
                    {
                        "message": f"Successfully deleted device from table. Deleted deviceID: {deviceID}"
                    }
                ),
                200
            )
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(
                jsonify(
                    {
                        "message": "The requested device does not exist."
                    }
                ),
                404
            )
            response.headers["Content-Type"] = "application/json"
            return response
    except Exception as e:
        response = make_response(
            jsonify(
                {
                    "message": f"Error occurred while checking for devices: {str(e)}"
                }
            ),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response


if __name__ == "__main__":
    app.run(port=8000)
    