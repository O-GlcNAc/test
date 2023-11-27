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

# Modify this part to read from FIFO and process the received data
with open('fifo', 'r') as fifo_file:
    while True:
        line = fifo_file.readline().strip()  # Read a line from FIFO
        if not line:
            continue

        sensor_id, reading = parse_sensor_data(line)  # Parse the received data

        with connection.cursor() as cursor:
            # Insert the parsed data into SensorData table
            sql = "INSERT INTO SensorData (sensor_id, reading, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(sql, (sensor_id, reading))

            # Get the recent 10 sensor readings
            sql_last_readings = "SELECT sensor_id FROM SensorData ORDER BY timestamp DESC LIMIT 10"
            cursor.execute(sql_last_readings)
            last_readings = [row['sensor_id'] for row in cursor.fetchall()]

            # Count occurrences of sensor_id in the last 10 readings
            id_counts = {id: last_readings.count(id) for id in set(last_readings)}

            # Check if the current sensor_id has appeared 2 or fewer times in the last 10 readings
            if id_counts.get(sensor_id, 0) <= 2:
                # Update SensorStatus table to set the sensor_id as 'disable'
                sql_update = "UPDATE SensorStatus SET status = 'disable', timestamp = CURRENT_TIMESTAMP WHERE sensor_id = %s"
                cursor.execute(sql_update, (sensor_id,))

        # Commit the changes to the database
        connection.commit()

        # Display the inserted data
        with connection.cursor() as cursor:
            sql = "SELECT * FROM SensorData WHERE sensor_id = %s AND reading = %s"
            cursor.execute(sql, (sensor_id, reading))
            result = cursor.fetchone()
            print(result)
