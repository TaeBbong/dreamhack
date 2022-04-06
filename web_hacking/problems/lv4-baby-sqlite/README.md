## 풀이

```python
sqli_filter = ['[', ']', ',', 'admin', 'select', '\'', '"', '\t', '\n', '\r', '\x08', '\x09', '\x00', '\x0b', '\x0d', ' ']
...
query = f"SELECT uid FROM users WHERE uid='{uid}' and upw='{upw}' and level={level};"
```

sql injection을 수행하는 문제

문제의 풀이는 3가지 스텝으로 구성되는데,

1. 어느 필드에 injection을 할 것인지
2. 목표 쿼리는 무엇인지
3. 목표 쿼리를 위해 필요한 필터링 우회는 무엇인지

일단 uid, upw, level을 보면 uid와 upw는 ''로 묶여 있는 반면, level은 그렇지 않다.
uid와 upw에서 injection을 하려면 '를 닫고 열어야 하는데, sqli_filter에 이미 '가 있기 때문에 이 두 필드에서 sql injection은 힘들다.
따라서 타겟 필드는 level로 정했다.

목표 쿼리는 union을 활용한다. 제시된 쿼리는 select uid로 필드 하나만 조회하며, 우리는 이미 admin이라는 uid를 알고 있기 때문에 union select로 쿼리를 작성할 필요 없이 그냥 union 'admin'을 구현하면 된다. 따라서 목표 쿼리는 

```sql
SELECT uid FROM users WHERE uid='dream' and upw='cometrue' and level=1 union 'admin';
```

여기서 level을 맞게 입력하면(9) dream 계정이 결과에 함께 나온다. 순서상 admin이 먼저 나오겠지만 그래도 혹시 모르니 틀리게 입력하는게 낫겠다.

이제 우회를 하면되는데, 우회할 대상은 공백과 'admin' 이다.
여기서 공백은 여러가지 방법이 있는데, '\x08', '\x09', '\x00', '\x0b', '\x0d', '/**/' 등이 있다.
이때 대부분 필터링에 걸리며, 가장 간단한 방법이 /**/ 주석을 활용하는 것이다.

그리고 'admin' 값은 char() 함수와 || 를 활용하면 만들어낼 수 있다.
values(char(97)||char(100)||char(109)||char(105)||char(110))
이렇게 하면 admin이 완성된다.

이걸 합하면

```python
level = '1/**/union/**/values(char(97)||char(100)||char(109)||char(105)||char(110))'
```

이라는 쿼리가 완성된다.