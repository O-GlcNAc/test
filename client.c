#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

#define FIFOFILE "fifo"

int main(int argc, char **argv) {
    int fd;
    srand(time(NULL)); // 난수 생성을 위한 시드 설정

    if ((fd = open(FIFOFILE, O_WRONLY)) < 0) { // FIFO를 쓰기 전용으로 열기
        perror("open()");
        return -1;
    }

    time_t start_time = time(NULL); // 현재 시간을 시작 시간으로 설정

    while (1) {
        int sensor_id = rand() % 3 + 1; // 1에서 3 사이의 랜덤 sensor_id 생성

        // 시간을 증가시키기 위해 현재 시간을 초 단위로 계산
        time_t current_time = time(NULL);
        current_time += 180; // 180초는 3분

        char timestamp_str[20]; // MariaDB timestamp 형식으로 저장할 문자열 버퍼
        strftime(timestamp_str, sizeof(timestamp_str), "%Y-%m-%d %H:%M:%S", localtime(&current_time));

        int temperature, humidity, illuminance;

        // sensor_id에 따라 온도, 습도, 조도 값을 설정
        if (sensor_id == 1) {
            temperature = rand() % 61 - 20; // sensor_id 1의 온도는 -20에서 40 사이 값
            humidity = rand() % 101;        // sensor_id 1의 습도는 0에서 100 사이 값
            illuminance = rand() % 1001;    // sensor_id 1의 조도는 0에서 1000 사이 값
        } else if (sensor_id == 2) {
            temperature = rand() % 101; // sensor_id 2의 온도는 0에서 100 사이 값
            humidity = rand() % 101;    // sensor_id 2의 습도는 0에서 100 사이 값
            illuminance = rand() % 1001; // sensor_id 2의 조도는 0에서 1000 사이 값
        } else {
            temperature = rand() % 21; // sensor_id 3의 온도는 0에서 20 사이 값
            humidity = rand() % 101;   // sensor_id 3의 습도는 0에서 100 사이 값
            illuminance = rand() % 1001; // sensor_id 3의 조도는 0에서 1000 사이 값
        }

        // FIFO로 sensor_id, timestamp_str, temperature, humidity, illuminance 데이터 전송
        dprintf(fd, "%d %s %d %d %d\n", sensor_id, timestamp_str, temperature, humidity, illuminance);

        // 3분 간격으로 데이터 전송
        usleep(180 * 1000000); // 180초를 마이크로초 단위로 변환

        // 시작 시간으로부터 1일(86400초) 이상 경과한 경우 종료
        if (difftime(current_time, start_time) >= 86400) { // difftime 함수를 사용하여 경과 시간 계산
            break;
        }
    }

    close(fd);
    return 0;
}
