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

    // 시작 날짜와 시간 설정 (23년 12월 1일 00시)
    struct tm start_time = {0};
    start_time.tm_year = 123; // 23년
    start_time.tm_mon = 11;   // 12월 (0부터 시작하므로 11은 12월)
    start_time.tm_mday = 1;   // 1일

    time_t current_time = mktime(&start_time); // 시작 시간을 time_t 형식으로 변환

    while (1) {
        int sensor_id = rand() % 3 + 1; // 1에서 3 사이의 랜덤 sensor_id 생성

        int timestamp = (int)current_time; // 현재 시간을 timestamp로 사용

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

        // FIFO로 sensor_id, timestamp, temperature, humidity, illuminance 데이터 전송
        dprintf(fd, "%d %d %d %d %d\n", sensor_id, timestamp, temperature, humidity, illuminance);

        // 3분씩 증가
        current_time += 180; // 180초는 3분

        // 0.3초 대기
        usleep(300000); // 300000 마이크로초 = 0.3초

        // 23년 12월 2일 00시까지의 데이터를 생성한 후 종료
        if (current_time >= mktime(&start_time) + 86400) { // 86400초는 하루의 초 단위 값
            break;
        }
    }

    close(fd);
    return 0;
}
