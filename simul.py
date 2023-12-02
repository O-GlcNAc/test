# 실제 환경에서 관측될 수 있는 계절성 및 일별 변동을 고려하여 시뮬레이션 데이터 생성
# 사인(sin) 및 코사인(cos) 함수를 활용하여 주기성을 부여하고, 가우시안 노이즈를 추가하여 현실적인 데이터 조정

import datetime
import random
import matplotlib.pyplot as plt
import math

# 기간 설정
start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)
end_date = datetime.datetime(2023, 1, 2, 0, 0, 0)
time_delta = datetime.timedelta(minutes=10)
timestamps = [start_date + i * time_delta for i in range(int((end_date - start_date) / time_delta))]

# 온도, 습도, 조도 생성
temperature = []
humidity = []
illuminance = []

for timestamp in timestamps:
    # 시간 기반의 주기성 부여
    hour = timestamp.hour
    day_of_year = timestamp.timetuple().tm_yday
    
    # 온도 데이터 생성
    temperature_noise = random.uniform(-2, 2)
    temperature.append(math.sin(math.pi * day_of_year / 365) * 5 + 25 + temperature_noise)
    
    # 습도 데이터 생성
    humidity_noise = random.uniform(-5, 5)
    humidity.append(math.cos(2 * math.pi * hour / 24) * 10 + 50 + humidity_noise)
    
    # 조도 데이터 생성
    illuminance_noise = random.uniform(-50, 50)
    illuminance.append(math.sin(2 * math.pi * hour / 24) * 250 + 750 + illuminance_noise)

# 그래프 그리기
plt.figure(figsize=(10, 5))
plt.plot(timestamps, temperature, label='Temperature (\'C)')
plt.plot(timestamps, humidity, label='Humidity (%)')
plt.plot(timestamps, illuminance, label='Illuminanace (lux)')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Simulated Temperature, Humidity, and Illuminance with Seasonal and Daily Variations')
plt.legend()
plt.grid(True)
plt.show()
