import mysql.connector as sql_connect
from mysql.connector import errorcode
from mysql.connector import (connection)
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

try:
    sql_connection = connection.MySQLConnection(
        user='root',
        host='127.0.0.1',
        database='final_project'
    )
    cursor = sql_connection.cursor(dictionary=True)
    # print("connected to database")

    query = ("select * from Customers where firstName = %s;")
    cursor.execute(query, ("John",))

    records = cursor.fetchall()

    print(records)

    # print(records)
    for record in records:
        print(f"First Name: {record['firstName']}\tLast Name: {record['lastName']}")

except sql_connect.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


@app.route('/login', methods=['POST'])
def authenticate_user():
    email = request.form['email']
    password = request.form['password']

    query = ("select exists (select * from Customers where email = %s)", (email,))
    cursor.execute(query)

    records = cursor.fetchall()

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
                    {"message": "Successfully authenticated user!"}
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
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    street_addr = request.form['streetAddr']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zipCode']

    query = ("select exists (select * from Customers where email = %s)", (email,))
    records = cursor.execute(query).fetchall()

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
        records = cursor.execute(last_id_query).fetchall()

        query = ("""insert into Customers (customerID, email, firstName, lastName, streetAddress, city, zipCode, state)
        values %s, %s, %s, %s, %s, %s, %s)""")
        try:
            cursor.execute(query, (int(records[0]['customerID']) + 1, email, first_name, last_name, street_addr, city, state, zip_code,))
            response = make_response(
                jsonify(
                    {"message": "User registered successfully!"}
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
    dateTakenOver = request.form['password']
    squareFootage = request.form['firstName']
    streetAddress = request.form['lastName']
    street_addr = request.form['streetAddr']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zipCode']
    unit = request.form['unit']
    numBedrooms = request.form['numBedrooms']
    numOccupants = request.form['numOccupants']

    query = ("select exists (select * from ServiceLocations where \
     streetAddress = %s and city = %s and zipCode = %s and state = %s and unit = %s)", (street_addr, city, zip_code, state, unit,))
    records = cursor.execute(query).fetchall()

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
        records = cursor.execute(last_id_query).fetchall()

        query = ("""insert into ServiceLocations (serviceLocID, customerID, dateTakenOver, squareFootage, streetAddress, city, zipCode, state, unit, numBedrooms, numOccupants)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
        try:
            cursor.execute(query, (int(records[0]['serviceLocID']) + 1, customerID, dateTakenOver, squareFootage, streetAddress, city, zip_code, state, unit, numBedrooms, numOccupants,))
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


@app.route('/getServiceLocations', methods=['POST'])
def get_service_locations():
    customerID = request.args.get("customerID")

    query = ("select * from ServiceLocations where customerID = %s;")
    serviceLocations = cursor.execute(query, (customerID,)).fetchall()

    total_service_loc_data = []

    if (serviceLocations):
        try:
            for sl in serviceLocations:
                serviceLocID = sl['serviceLocID']

                query = ("select * from Devices where serviceLocID = %s;")
                device_records = cursor.execute(query, (serviceLocID,)).fetchall()
                total_price_to_date = 0
                total_devices = 0

                total_devices_by_type = {}

                for device in device_records:
                    deviceID = device['deviceID']

                    query = ("""select * (ec.totalEnergyConsumed * ep.price) as deviceCost from EnergyConsumption ec
                        join EnergyPrices ep on ec.priceTimeID = ep.priceTimeID
                        where ec.deviceID = %s
                        group by ec.eventTimestamp;""")
                    energy_consumption_records = cursor.execute(query, (deviceID,)).fetchall()

                    cost_for_device = 0

                    for rec in energy_consumption_records:
                        cost_for_device += float(rec['deviceCost'])
                
                    total_price_to_date += cost_for_device
                    total_devices += 1

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
                    "totalDevices": totalDevices,
                    "totalDevicesByType": total_devices_by_type
                }

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

    











# @app.route('/addDevice', methods=['POST'])
# def add_device_to_service_location():
    