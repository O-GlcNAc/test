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

    char timestamp_str[20]; // MariaDB timestamp 형식으로 저장할 문자열 버퍼

    while (1) {
        // ...

        strftime(timestamp_str, sizeof(timestamp_str), "%Y-%m-%d %H:%M:%S", localtime(&current_time));

        // FIFO로 sensor_id, timestamp_str, temperature, humidity, illuminance 데이터 전송
        dprintf(fd, "%d %s %d %d %d\n", sensor_id, timestamp_str, temperature, humidity, illuminance);

        // ...

        current_time += 180; // 180초는 3분

        // ...
    }

    close(fd);
    return 0;
}
