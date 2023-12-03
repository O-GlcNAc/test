import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='scott',
                             password='tiger',
                             database='mydb',
                             cursorclass=pymysql.cursors.DictCursor)

# Assume the received data is in the format: "sensor_id timestamp temperature humidity illuminance\n"
def parse_sensor_data(data):
    parts = data.strip().split()
    sensor_id = int(parts[0])
    timestamp = int(parts[1])
    temperature = float(parts[2])
    humidity = float(parts[3])
    illuminance = float(parts[4])
    return sensor_id, timestamp, temperature, humidity, illuminance

# Modify this part to read from FIFO and process the received data
with open('fifo', 'r') as fifo_file:
    while True:
        line = fifo_file.readline().strip()  # Read a line from FIFO
        if not line:
            continue

        sensor_id, timestamp, temperature, humidity, illuminance = parse_sensor_data(line)  # Parse the received data

        with connection.cursor() as cursor:
            # Insert the parsed data into SensorData table
            sql = "INSERT INTO SensorData (sensor_id, timestamp, temperature, humidity, illuminance) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (sensor_id, timestamp, temperature, humidity, illuminance))

            # Get the last sensor readings for the current sensor_id
            sql_last_readings = "SELECT sensor_id FROM SensorData WHERE sensor_id = %s ORDER BY timestamp DESC LIMIT 10"
            cursor.execute(sql_last_readings, (sensor_id,))
            last_readings = [row['sensor_id'] for row in cursor.fetchall()]

            # Check if the current sensor_id has appeared 3 times non-sequentially
            if len(last_readings) < 10 or last_readings.count(sensor_id) > 2:
                # Update SensorStatus table to set the sensor_id as 'available'
                sql_update = "UPDATE SensorStatus SET status = 'available', timestamp = CURRENT_TIMESTAMP WHERE sensor_id = %s"
                cursor.execute(sql_update, (sensor_id,))
            else:
                # Update SensorStatus table to disable the sensor_id
                sql_update = "UPDATE SensorStatus SET status = 'disable', timestamp = CURRENT_TIMESTAMP WHERE sensor_id = %s"
                cursor.execute(sql_update, (sensor_id,))

        # Commit the changes to the database
        connection.commit()

        # Display the inserted data
        with connection.cursor() as cursor:
            sql = "SELECT * FROM SensorData WHERE sensor_id = %s AND timestamp = %s AND temperature = %s AND humidity = %s AND illuminance = %s"
            cursor.execute(sql, (sensor_id, timestamp, temperature, humidity, illuminance))
            result = cursor.fetchone()
            print(result)
