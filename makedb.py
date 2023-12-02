# 이때 mariadb서버는 켜져 있어야한다.


import mysql.connector

# MariaDB 연결 설정
conn = mysql.connector.connect(
    host='localhost',
    user='scott',
    password='tiger'
)

# 커서 생성
cursor = conn.cursor()

# exam 데이터베이스 생성
cursor.execute("CREATE DATABASE IF NOT EXISTS exam")
print("exam 데이터베이스가 생성되었습니다.")

# exam 데이터베이스 선택
cursor.execute("USE exam")

# Sensors 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sensors (
        id INTEGER PRIMARY KEY,
        name VARCHAR(30),
        location VARCHAR(50)
    )
""")
print("Sensors 테이블이 생성되었습니다.")

# SensorData 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SensorData (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        sensor_id INTEGER,
        reading FLOAT,
        timestamp TIMESTAMP,
        temperature FLOAT,
        humidity FLOAT,
        light FLOAT,
        FOREIGN KEY (sensor_id) REFERENCES Sensors(id)
    )
""")
print("SensorData 테이블이 생성되었습니다.")

# Sensorstatus 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sensorstatus (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        sensor_id INTEGER,
        status VARCHAR(10),
        timestamp TIMESTAMP,
        FOREIGN KEY (sensor_id) REFERENCES Sensors(id)
    )
""")
print("Sensorstatus 테이블이 생성되었습니다.")

# 커밋 및 연결 종료
conn.commit()
conn.close()
