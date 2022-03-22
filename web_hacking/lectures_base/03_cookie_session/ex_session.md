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
            session_id = os.urandom(32).hex()
            session_storage[session_id] = username
            resp.set_cookie('sessionid', session_id)
            return resp 
        return '<script>alert("wrong password");history.go(-1);</script>'


@app.route('/admin')
def admin():
    return session_storage


if __name__ == '__main__':
    import os
    session_storage[os.urandom(32).hex()] = 'admin'
    print(session_storage)
    app.run(host='0.0.0.0', port=8000)
```

## 풀이

처음에는 main에서 session_storage를 출력하기 때문에 이를 nc를 통해 받아올 수 있지 않을까 생각했는데,
nc에서는 웹 포트만 오픈되어 있기 때문에 interaction을 만들 수 없었다.

또한 일부 문제는 random에서 고정 상수 값을 사용해서 같은 문자열이 나오는 경우도 있는데,
이 문제의 경우는 제시된 string인 admin을 활용하지 않는 랜덤 함수에, 매번 달라지는 랜덤 값이므로 이 또한 적용되지 않았다.

그런 와중에 코드에서 미처 보지 못한 @app.route('/admin') 라우팅을 보았고,
여기서 너무 간단하게 session_storage를 노출하고 있어서 여기서 admin의 session_id를 가져올 수 있었다.

크롬 개발자 도구에서 session에 해당 session_id를 입력하고 새로 고침하면 admin의 패스워드인 Flag를 얻을 수 있었다.