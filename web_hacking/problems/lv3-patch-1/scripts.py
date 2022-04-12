import requests

session = requests.session()

def login(userid, password):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = session.post("http://localhost:8080/api/login", data={"userid": userid, "password": password}, headers=headers)

    print(res.text)

def memo_add():
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = session.put("http://localhost:8080/api/memo/add", data={"title": "title", "contents": "{{config}}"}, headers=headers)

    print(res.text)

if __name__ == "__main__":
    login("testuser", "testuser")
    memo_add()