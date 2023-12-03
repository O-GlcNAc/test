#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h> // 오류 메시지 출력을 위해 추가

#define FIFOFILE "fifo"
#define PYTHON_SCRIPT "/home/minwoo/test/mydb.py" // 'mydb.py' 파일의 절대 경로로 변경

int main(int argc, char **argv) {
    int fd;
    char buf[BUFSIZ];

    unlink(FIFOFILE); // 기존 FIFO 파일 삭제

    if (mkfifo(FIFOFILE, 0666) < 0) { // 새로운 FIFO 파일 생성
        perror("mkfifo()");
        return -1;
    }

    if ((fd = open(FIFOFILE, O_RDONLY)) < 0) { // FIFO를 읽기 전용으로 열기
        perror("open()");
        return -1;
    }

    FILE *fp;
    char command[BUFSIZ];

    while (1) {
        int n = read(fd, buf, sizeof(buf)); // FIFO로부터 데이터를 읽음

        if (n > 0) {
            buf[n] = '\0'; // Null-terminate 문자열

            // 파이썬 스크립트를 호출하여 FIFO로부터 받은 데이터를 전달하고 MariaDB에 데이터 삽입
            snprintf(command, sizeof(command), "python3 %s \"%s\"", PYTHON_SCRIPT, buf);
            fp = popen(command, "r"); // 쓰기 전용으로 파일 포인터 열기
            if (fp == NULL) {
                printf("Failed to execute Python script: %s\n", strerror(errno)); // 오류 메시지 출력
                return -1;
            }

            char result_buffer[1024]; 

            while (fgets(result_buffer, sizeof(result_buffer), fp) != NULL) {
                printf("%s", result_buffer); // 파이썬 스크립트의 출력 결과를 터미널에 출력
            }

            // 파이썬 스크립트의 실행 결과
            printf("Data sent to Python script for database insertion.\n");
            pclose(fp); // 파일 포인터 닫기
        }
    }

    close(fd);
    return 0;
}
