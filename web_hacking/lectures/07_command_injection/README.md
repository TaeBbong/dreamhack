## Command Injection

### Intro

웹 개발 중 시스템 함수를 사용하는 경우가 간혹 있음
PHP(system), Node.js(child_process), Python(os.system) 등

### Command Injection

이용자의 입력을 시스템 명령어로 실행하게 하는 취약점
명령어를 실행하는 함수에 이용자가 임의의 인자를 전달할 수 있을 때 발생

```bash
`` => 명령어 치환
$() => 명령어 치환
&& => 명령어 연속 실행(AND, 앞에서 에러 발생하지 않아야 뒷 명령어 실행)
|| => 명령어 연속 실행(OR, 앞에서 에러 발생해야 뒷 명령어 실행) 
; => 명령어 에러 상관 없이 실행
| => 앞 명령어의 결과가 뒷 명령어 입력으로 들어감
```
