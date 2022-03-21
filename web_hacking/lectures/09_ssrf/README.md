## SSRF

### 마이크로서비스

소규모의 독립적인 서비스로 서버를 구성하느 방법
각기 다른 마이크로 서비스끼리 HTTP 통신 발생

### Server-side Request Forgery(SSRF)

웹서비스의 권한으로 공격자가 서버에 요청을 보내는 것
웹서비스의 권한이기 때문에 서버 입장에서는 정상 요청이라 생각하고 처리
이때 백오피스(관리자 페이지) 쪽으로 요청을 보낼 수 있다면
공격자는 백오피스에 접근할 수 있게 됨

### 이용자가 입력한 URL에 요청을 보내는 경우

```python
# pip3 install flask requests # 파이썬 flask, requests 라이브러리를 설치하는 명령입니다.
# python3 main.py # 파이썬 코드를 실행하는 명령입니다.
from flask import Flask, request
import requests
app = Flask(__name__)
@app.route("/image_downloader")
def image_downloader():
    # 이용자가 입력한 URL에 HTTP 요청을 보내고 응답을 반환하는 페이지 입니다.
    image_url = request.args.get("image_url", "") # URL 파라미터에서 image_url 값을 가져옵니다.
    response = requests.get(image_url) # requests 라이브러리를 사용해서 image_url URL에 HTTP GET 메소드 요청을 보내고 결과를 response에 저장합니다.
    return ( # 아래의 3가지 정보를 반환합니다.
        response.content, # HTTP 응답으로 온 데이터
        200, # HTTP 응답 코드
        {"Content-Type": response.headers.get("Content-Type", "")}, # HTTP 응답으로 온 헤더 중 Content-Type(응답 내용의 타입)
    )
@app.route("/request_info")
def request_info():
    # 접속한 브라우저(User-Agent)의 정보를 출력하는 페이지 입니다.
    return request.user_agent.string
app.run(host="127.0.0.1", port=8000)
```

위와 같은 경우 image_url에 임의의 경로를 입력할 수 있음
/image_downloader?image_url=http://127.0.0.1:8000/request_info

이렇게 하면 request_info에 요청을 보낼 수 있음

### 웹 서비스의 요청 URL에 이용자의 입력값이 포함되는 경우

```python
INTERNAL_API = "http://api.internal/"
# INTERNAL_API = "http://172.17.0.3/"
@app.route("/v1/api/user/information")
def user_info():
	user_idx = request.args.get("user_idx", "")
	response = requests.get(f"{INTERNAL_API}/user/{user_idx}")
@app.route("/v1/api/user/search")
def user_search():
	user_name = request.args.get("user_name", "")
	user_type = "public"
	response = requests.get(f"{INTERNAL_API}/user/search?user_name={user_name}&user_type={user_type}")
```

이런 경우 url을 조작할 수 있기 때문에 Path Traversal을 활용할 수 있음

{INTERNAL_API}/user/{user_idx}에서 user_idx에 ../search를 넣으면
{INTERNAL_API}/search 를 실행시킬 수 있음

혹은 http://api.internal/search?user_name=secret&user_type=private#&user_type=public를 통해 뒤의 url을 주석처리할 수 있음

### 웹서비스의 요청 Body에 이용자의 입력값이 포함되는 경우

```python
from flask import Flask, request, session
import requests
from os import urandom
app = Flask(__name__)
app.secret_key = urandom(32)
INTERNAL_API = "http://127.0.0.1:8000/"
header = {"Content-Type": "application/x-www-form-urlencoded"}
@app.route("/v1/api/board/write", methods=["POST"])
def board_write():
    session["idx"] = "guest" # session idx를 guest로 설정합니다.
    title = request.form.get("title", "") # title 값을 form 데이터에서 가져옵니다.
    body = request.form.get("body", "") # body 값을 form 데이터에서 가져옵니다.
    data = f"title={title}&body={body}&user={session['idx']}" # 전송할 데이터를 구성합니다.
    response = requests.post(f"{INTERNAL_API}/board/write", headers=header, data=data) # INTERNAL API 에 이용자가 입력한 값을 HTTP BODY 데이터로 사용해서 요청합니다.
    return response.content # INTERNAL API 의 응답 결과를 반환합니다.
@app.route("/board/write", methods=["POST"])
def internal_board_write():
    # form 데이터로 입력받은 값을 JSON 형식으로 반환합니다.
    title = request.form.get("title", "")
    body = request.form.get("body", "")
    user = request.form.get("user", "")
    info = {
        "title": title,
        "body": body,
        "user": user,
    }
    return info
@app.route("/")
def index():
    # board_write 기능을 호출하기 위한 페이지입니다.
    return """
        <form action="/v1/api/board/write" method="POST">
            <input type="text" placeholder="title" name="title"/><br/>
            <input type="text" placeholder="body" name="body"/><br/>
            <input type="submit"/>
        </form>
    """
app.run(host="127.0.0.1", port=8000, debug=True)
```

이 경우 title, body, user를 파라미터 형식으로 설정하기 때문에 &를 활용하면 data 값을 변조할 수 있음

title=title&user=admin을 넣으면

title=title&user=admin&body=body&user=guest
이런식으로 넣을 수 있고,
순서대로 값을 참조하기 때문에 user에는 guest가 아닌 admin이 들어간다.

