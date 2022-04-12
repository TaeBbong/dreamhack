## 풀이

간단한 플라스크 웹 어플리케이션을 보안 패치하는 문제
지금 하고 있는 일과 연관되어 있기 때문에 더욱 흥미 있게 풀었고,
최근에 플라스크를 정말 많이 봤기 때문에 나름 자신 있었다.

일단 문제에서 체커를 실행하면 다음과 같이 나타난다.

```markdown
[FAIL]
 - SLA(7/7): SLA PASS
 - VULN(5)
   - Hard-coded Key
   - SQL Injection
   - Server-Side Template Injection
   - Cross Site Scripting
   - Memo Update IDOR
```

친절하게 취약점 목록이 나타나는데,
semgrep 툴을 통해 돌렸을 때는 SQL Injection과 SSTI, XSS만 나타났다.

아무튼 패치를 진행해보자.

### 1. Hard-coded Key

```python
app.secret_key = 'secret_key'
```

와 같이 키 값이 고정으로 저장되어 있다.
일반적으로는 env 파일이나 config 파일을 만들어서 저장한 다음 불러오는 방식으로 사용하는데,
우리는 현재 외부 파일을 생성할 수 없고 오직 app.py만 수정할 수 있어서 어떻게 할까 싶었다.
이때 우리는 굳이 secret_key 값을 원하는 값으로 설정할 필요가 없기 때문에
드림핵의 다른 문제 파일들에서 그랬듯 랜덤한 문자열로 채우면 된다.

```python
app.secret_key = os.urandom(32)
```

### 2. SSTI & XSS

```python
template = ''' Written by {userid}<h3>{title}</h3>
<pre>{contents}</pre>
'''.format(title=title, userid=userid, contents=contents)
```

render_template_string()을 활용한 SSTI 취약점 및 XSS 취약점이 가능하다.
SSTI 취약점을 막기 위해서는 가장 기본적으로는 필터링이 있는데, 몇번 시도했지만 필터링으로는 해결이 되지 않는다.
그래서 알아본 결과, 다음과 같은 방법으로 패치할 수 있다.

```python
context = {
    'userid': userid,
    'title': title,
    'contents': contents
}

if mode == 'html':
    template = '''Written by {{userid}}<h3>{{title}}</h3>
    <pre>{{contents}}</pre>
    '''
    return render_template_string(template, **context)
```

이런 식으로 딕셔너리 형태로 variable을 render_template_string()의 인자로 전달하면 autoescape가 수행되면서 방어가 가능하다.

### 3. SQL Injection

```python
ret = query_db(f"SELECT * FROM users where userid='{userid}' and password='{hashlib.sha256(password.encode()).hexdigest()}'" , one=True)
...
ret = query_db("SELECT * FROM memo where idx=" + idx)[0]
```

위처럼 + 방식으로 인자를 전달하게 되면 SQL Injection이 발생할 수 있다.
SQL Injection은 orm을 쓰는게 가장 안전한 방법이지만 더 쉬운 방법이 있다.
친절하게도 문제에서 방법을 제시해주었다.

```python
ret = query_db('SELECT * FROM memo where idx=?', [idx,])[0]
```

와 같이 ?를 활용해서 인자를 전달하면 이는 SQL Injection으로부터 안전해진다.
왜인지는 아직 모름...

### 4. IDOR(Insecure Direct Object Reference)

IDOR는 결국 권한이 설정되지 않았거나 잘못 설정되어 오브젝트에 의도치 않은 유저가 접근할 수 있는 것을 의미한다.
딱 봐도 회원 정보 조회용 api 또는 게시글 수정 관련 기능에서 발생할 것으로 생각됐다.
(왜냐면 내가 개발할 때 자주 놓치기 때문에..)

역시 memoUpdate 쪽에서 로그인 검증은 하는데 작성자 검증을 안하고 있었다.
간단히 조건문을 추가하여 차단하도록 하자.

```python
@app.route('/api/memo/<int:idx>', methods=['PUT'])
def memoUpdate(idx):
  if not session.get('uid'):
    return jsonify(result="no login")

  ...

  if userid != ret['userid']:
    return jsonify(result="no permission")
```