#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>

#define FIFOFILE "fifo"

int main(int argc, char **argv)
{
    int n, fd;
    char buf[BUFSIZ];

    if((fd = open(FIFOFILE, O_WRONLY)) < 0) { 		/* FIFO를 연다. */
        perror("open()");
        return -1;
    }

    while (1) {
        // 랜덤 텍스트 생성
        for (int i = 0; i < 3; ++i) {
            buf[i] = 'A' + rand() % 26; // 랜덤 알파벳 생성
        }
        buf[BUFSIZ - 1] = '\0'; // 문자열 종료

        // FIFO로 데이터 보내기
        write(fd, buf, BUFSIZ);

        sleep(1); // 1초 대기
    }

    return 0;
}
