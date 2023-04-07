import os

def level0():
    answer = ''
    # [0] answer: Th1s_1s_Adm1n_P@SS
    # sql injection 패턴을 확인, blind sql injection으로 하는 것으로 보여, status code가 다른 것을 확인(500)
    with open("access.log", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "GET /board.php?sort=if(ord(substr((select%20group_concat(username" in line:
                status = line.split('HTTP/1.1" ')[1][0:3]
                if status != "200":
                    answer += chr(int(line.split('))=')[1].split(',')[0]))
    print(f"[0] answer: {answer.split(':')[1].split(',')[0]}")
    return

def level1():
    # [1] answer: php://filter/convert.base64-encode/resource=../config.php
    # 200 OK 확인
    answer = 'php://filter/convert.base64-encode/resource=../config.php'
    print(f"[1] answer: {answer}")
    return

def level2():
    # [2] answer: /var/lib/php/sessions/sess_ag4l8a5tbv8bkgqe9b9ull5732
    # 200 OK 확인
    answer = '/var/lib/php/sessions/sess_ag4l8a5tbv8bkgqe9b9ull5732'
    print(f"[2] answer: {answer}")
    return

def level3():
    # [3] answer: /var/www/html/uploads/images.php
    # access log에서 웹쉘 페이로드로 의심되는 것을 발견
    # urldecoding 후 php 파일 원본 확인
    # 날짜를 로그에 찍힌 날짜로 넣고, php 파일을 실행하면 file_put_contents(/var/www/html/uploads/images.php)를 실행하는 것을 알 수 있음
    # 이를 통해 웹쉘이 해당 경로에 생성되었음을 알 수 있음
    answer = '/var/www/html/uploads/images.php'
    print(f"[3] answer: {answer}")
    return

def level4():
    # [4] answer: whoami
    # images.php를 검색하면 whoami 로그가 나옴
    answer = 'whoami'
    print(f"[4] answer: {answer}")
    return

if __name__ == "__main__":
    level0()
    level1()
    level2()
    level3()
    level4()