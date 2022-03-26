## 코드

```python
#!/usr/bin/python3
from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)

try:
    FLAG = open('./flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

users = {
    'guest': 'guest',
    'user': 'user1234',
    'admin': FLAG
}

session_storage = {
}

@app.route('/')
def index():
    session_id = request.cookies.get('sessionid', None)
    try:
        username = session_storage[session_id]
    except KeyError:
        return render_template('index.html')

    return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not admin"}')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            pw = users[username]
        except:
            return '<script>alert("not found user");history.go(-1);</script>'
        if pw == password:
            resp = make_response(redirect(url_for('index')) )
            session_id = os.urandom(4).hex()
            session_storage[session_id] = username
            resp.set_cookie('sessionid', session_id)
            return resp 
        return '<script>alert("wrong password");history.go(-1);</script>'

if __name__ == '__main__':
    import os
    session_storage[os.urandom(1).hex()] = 'admin'
    print(session_storage)
    app.run(host='0.0.0.0', port=8000)
```

## 풀이

기본적인 세션/쿠키 문제인데, login 로직까지만 봤을때는 정상적으로 보였다.
어떻게 풀지 싶던 와중, main에서 이런 코드를 발견했다.

```python
session_storage[os.urandom(1).hex()] = 'admin'
```

os.urandom(1).hex()는 분명 짧은 문자열일 것이다는 생각에, 파이썬으로 실행시켜보니
16진수 두자리 값임을 알 수 있었다!

따라서 이 값을 얻어낸 다음 request headers의 cookie에 sessionid에다가 해당 2자리 값을 넣으면
admin으로 로그인이 가능해진다!
이를 스크립트로 작성해서 해결했다.