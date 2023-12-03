#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h> // 오류 메시지 출력을 위해 추가

#define FIFOFILE "fifo"
#define PYTHON_SCRIPT "mydb.py" // 'mydb.py' 파일의 절대 경로로 변경

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

    while (1) {
        int n = read(fd, buf, sizeof(buf)); // FIFO로부터 데이터를 읽음

        if (n > 0) {
            buf[n] = '\0'; // Null-terminate 문자열

            // 파이썬 스크립트를 호출하여 FIFO로부터 받은 데이터를 전달하고 MariaDB에 데이터 삽입
            fp = popen(PYTHON_SCRIPT, "w"); // 쓰기 전용으로 파일 포인터 열기
            if (fp == NULL) {
                fprintf(stderr, "Failed to execute Python script: %s\n", strerror(errno)); // 오류 메시지 출력
                return -1;
            }

            // FIFO로부터 받은 데이터를 파이썬 스크립트에 쓰기
            fwrite(buf, sizeof(char), strlen(buf), fp);
            pclose(fp); // 파일 포인터 닫기

            // 파이썬 스크립트의 실행 결과는 터미널에서 직접 확인할 수 있도록 변경하였습니다.
            printf("Data sent to Python script for database insertion.\n");
        }
    }

    close(fd);
    return 0;
}
