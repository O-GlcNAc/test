import pymysql

# MariaDB 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='scott',  # root 계정으로 접속합니다. 적절한 권한을 가진 계정으로 변경하세요.
    password='tiger',  # root 계정의 비밀번호를 입력하세요.
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

# 'scott' 사용자에게 'exam' 데이터베이스에 대한 권한 부여
cursor.execute("GRANT ALL PRIVILEGES ON exam.* TO 'scott'@'localhost'")

# 커밋 및 연결 종료
conn.commit()
conn.close()
