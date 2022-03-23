## 코드

```python
@app.route('/get_info', methods=['GET', 'POST'])
def get_info():
    if request.method == 'GET':
        return render_template('get_info.html')
    elif request.method == 'POST':
        userid = request.form.get('userid', '')
        info = requests.get(f'{API_HOST}/api/user/{userid}').text
        return render_template('get_info.html', info=info)

@app.route('/api/flag')
@internal_api
def flag():
    return FLAG
```

## 풀이

외부 요청을 통해 내부 API를 호출 시키는 것!
get_info()에서 requests.get({API_HOST}/api/user/{userid})와 같이 요청을 보내므로,
userid에 ../flag를 넣으면 끝

근데 그냥 입력창에 ../flag를 넣으면 잘 동작하지 않는데,
이는 입력창에 username을 입력하면 그즉시 userid(0, 1)로 바뀌기 때문이다.

```python
@app.route('/api/user/<uid>')
@internal_api
def get_flag(uid):
    try:
        info = users[uid]
    except:
        info = {}
    return json.dumps(info)
```

이걸 먼저 실행시키기 때문인듯

따라서 버프로 패킷을 잡아서 ../flag를 삽입해주면 플래그가 나타난다.