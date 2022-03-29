## 코드

```python
#app.py
import socket
import requests
import ipaddress
from urllib.parse import urlparse
from flask import Flask, request, render_template

app = Flask(__name__)
app.flag = '__FLAG__'

def lookup(url):
    try:
        return socket.gethostbyname(url)
    except:
        return False

def check_global(ip):
    try:
        return (ipaddress.ip_address(ip)).is_global
    except:
        return False

def check_get(url):
    ip = lookup(urlparse(url).netloc)
    if ip == False or ip =='0.0.0.0':
        return "Not a valid URL."
    res=requests.get(url)
    if check_global(ip) == False:
        return "Can you access my admin page~?"
    for i in res.text.split('>'):
        if 'referer' in i:
            ref_host = urlparse(res.headers.get('refer')).netloc
            if ref_host == 'localhost':
                return False
            if ref_host == '127.0.0.1':
                return False 
    res=requests.get(url)
    return res.text

@app.route('/admin')
def admin_page():
    if request.remote_addr != '127.0.0.1':
    		return "This is local page!"
    return app.flag

@app.route('/validation')
def validation():
    url = request.args.get('url', '')
    ip = lookup(urlparse(url).netloc)
    res = check_get(url)
    return render_template('validation.html', url=url, ip=ip, res=res)

@app.route('/')
def index():
    return render_template('index.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=3333)
```

## 풀이

/validation

url을 인자로 받아서
ip = lookup(url)로 ip 주소를 따고,
res = check_get(url)을 실행시킴

check_get(url)
url을 인자로 받아서
ip = lookup(url)로 ip 주소를 딴 다음 ip 주소 유효성 확인하고
res = requests.get(url)로 데이터 가져온 다음,
ip가 공인 IP인지 확인하고 아니면 fail => SSRF 방지(이거 안하면 127.0.0.1:3333/admin 주소 넣어서 클리어 가능)
res.text 안에서 referer가 있는지 본 다음에,
그 refer가 localhost이거나 127.0.0.1이면 fail
이후 결과를 return

/admin
remote_addr이 127.0.0.1이 아니면 fail
맞으면 flag return

/validation에 어떤 url을 던져서
check_get(url)을 통과하고,
requests.get(url)을 했는데 이게 /admin으로 가는데
remote_addr을 127.0.0.1로 만들어서 보내면 된다....


가장 기본적인 생각은

host1.dreamhack.games:21686/validation?url=host1.dreamhack.games:21686/admin
을 보낼건데
refer를 LocalHost로 설정하고
remote_addr을 127.0.0.1로 설정

이렇게 생각하고 요청을 보내봤는데 역시나 안된다.
기본적으로 url에 문제 url을 넣으면 터지는 거 같음

일단 결국 미션은 127.0.0.1:3333/admin으로 접속하게 만드는 것이다.
근데 공인 IP 쪽을 우회해야 하므로 우회 방법을 찾아야 한다. => SSRF 방어를 우회하는 기법 중 리다이렉션, 단축 URL 등의 방법이 있음
이 과정에서 몇가지 조사를 해보니

http://google.com:80@127.0.0.1:3333/admin

이렇게 trust page@untrust page로 우회하는 경우가 있었다.

또한 URL 단축 서비스를 활용해서

https://han.gl/GcZDX

이렇게 만드는 경우도 있었다.

하면 할 수록 모르는 내용이 많다.. 배경지식이 많이 필요한 것 같다.

(추가) 이런 방법도 있다더라..

DNS Rebinding

https://m.blog.naver.com/tkdldjs35/221307513668