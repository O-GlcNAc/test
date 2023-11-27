import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='scott',
                             password='tiger',
                             database='mydb',
                             cursorclass=pymysql.cursors.DictCursor)

# Assume the received data is in the format: "sensor_id reading\n"
def parse_sensor_data(data):
    sensor_id, reading = data.strip().split()
    return int(sensor_id), float(reading)

# Define a function to check if a given sensor ID is disabled
def check_disabled_status(cursor, sensor_id):
    sql = "SELECT status FROM SensorStatus WHERE sensor_id = %s"
    cursor.execute(sql, (sensor_id,))
    result = cursor.fetchone()
    return result['status'] == 'disable'

# Modify this part to read from FIFO and process the received data
with open('fifo', 'r') as fifo_file:
    while True:
        line = fifo_file.readline().strip()  # Read a line from FIFO
        if not line:
            continue

        sensor_id, reading = parse_sensor_data(line)  # Parse the received data
        timestamp = None  # Since the timestamp is automatically added, no need to specify here

        with connection.cursor() as cursor:
            # Insert the parsed data into SensorData table
            sql = "INSERT INTO SensorData (sensor_id, reading, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(sql, (sensor_id, reading))

            # Get the last 5 sensor readings for the current sensor_id
            sql_last_readings = "SELECT sensor_id FROM SensorData ORDER BY timestamp DESC LIMIT 5"
            cursor.execute(sql_last_readings)
            last_readings = [row['sensor_id'] for row in cursor.fetchall()]

            # Check if the current sensor_id has appeared 3 times non-sequentially
            if last_readings.count(sensor_id) < 3:
                if check_disabled_status(cursor, sensor_id):
                    continue
                else:
                    # Update SensorStatus table to disable the sensor_id
                    sql_update = "UPDATE SensorStatus SET status = 'disable', timestamp = CURRENT_TIMESTAMP WHERE sensor_id = %s"
                    cursor.execute(sql_update, (sensor_id,))
            else:
                # Update SensorStatus table to set the sensor_id as 'available'
                sql_update = "UPDATE SensorStatus SET status = 'available', timestamp = CURRENT_TIMESTAMP WHERE sensor_id = %s"
                cursor.execute(sql_update, (sensor_id,))

        # Commit the changes to the database
        connection.commit()

        # Display the inserted data
        with connection.cursor() as cursor:
            sql = "SELECT * FROM SensorData WHERE sensor_id = %s AND reading = %s"
            cursor.execute(sql, (sensor_id, reading))
            result = cursor.fetchone()
            print(result)
