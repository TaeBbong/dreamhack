## 코드

```python
#!/usr/bin/python3
from flask import (
    Flask,
    request,
    render_template
)
import http.server
import threading
import requests
import os, random, base64
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.urandom(32)

try:
    FLAG = open("./flag.txt", "r").read()  # Flag is here!!
except:
    FLAG = "[**FLAG**]"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/img_viewer", methods=["GET", "POST"])
def img_viewer():
    if request.method == "GET":
        return render_template("img_viewer.html")
    elif request.method == "POST":
        url = request.form.get("url", "")
        urlp = urlparse(url)
        if url[0] == "/":
            url = "http://localhost:8000" + url
        elif ("localhost" in urlp.netloc) or ("127.0.0.1" in urlp.netloc):
            data = open("error.png", "rb").read()
            img = base64.b64encode(data).decode("utf8")
            return render_template("img_viewer.html", img=img)
        try:
            data = requests.get(url, timeout=3).content
            img = base64.b64encode(data).decode("utf8")
        except:
            data = open("error.png", "rb").read()
            img = base64.b64encode(data).decode("utf8")
        return render_template("img_viewer.html", img=img)


local_host = "127.0.0.1"
local_port = random.randint(1500, 1800)
local_server = http.server.HTTPServer(
    (local_host, local_port), http.server.SimpleHTTPRequestHandler
)


def run_local_server():
    local_server.serve_forever()


threading._start_new_thread(run_local_server, ())

app.run(host="0.0.0.0", port=8000, threaded=True)
```

## 풀이

localhost:{RANDOM_PORT}/에서 simpleHTTPServer가 돌아가고 있다.
여기에 flag.txt가 있을 것이므로,
image_viewer의 url에 localhost:{RANDOM_PORT}/flag.txt 를 성공하면 되는데,
이때 필터링에서 localhost, 127.0.0.1을 필터링한다.
로컬호스트 주소는 LoCaLhost처럼 우회하거나, 127.0.0.222와 같이 우회할 수 있다.
랜덤 포트는 1500~1800이므로 스크립트로 다 돌려보면 된다.

포트를 얻고 요청은

http://Localhost:1590/flag.txt를 하면 된다.
그러면 이미지가 깨진 채로 나오는데,
페이지 소스를 보면 base64 인코딩으로 나오므로, 디코딩 시키면 플래그가 나온다.
이또한 코드에 나와있는 내용이다! 코드를 자세히 보자..