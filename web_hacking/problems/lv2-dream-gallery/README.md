# 풀이

```python
@app.route('/request')
def url_request():
    url = request.args.get('url', '').lower()
    title = request.args.get('title', '')
    if url == '' or url.startswith("file://") or "flag" in url or title == '':
        return render_template('request.html')

    try:
        data = urlopen(url).read()
        mini_database.append({title: base64.b64encode(data).decode('utf-8')})
        return redirect(url_for('view'))
    except:
        return render_template("request.html")
```

문제의 모든 부분, urlopen을 통해 서버 내부의 파일을 읽어오는 것이 핵심
파일을 읽기 위해 다양한 방식을 시도했는데, http:// uri로는 해결이 안된다.
http://localhost/view 와 같이 페이지 소스를 읽어올 수는 있지만, 어차피 Path Traversal이 안되기 때문에 flag.txt에 접근할 수 없다.
문제의 필터링이 그 힌트가 되는데, file://로 시작하는 것을 필터링하는 것이다.
이는 file:// 앞에 공백 하나로 우회가 된다.
마지막은 flag 우회인데, 이는 urlencoding으로 우회 가능하다.
파일을 읽을 때 urlopen이 동작하기 때문에 가능한 일이다.

페이로드는 다음과 같다.

` file:///%66%6c%61%67%2e%74%78%74`

핵심은 사용하는 라이브러리, 함수를 따라가면서 어떤 식으로 동작하는지 분석한 것
urlopen()에서 쓰는 unwrap()은 <>를 제거하는 절차가 있으므로 <file://...> 와 같이 우회할 수도 있을 것이다.
또한 unquote()도 동작하므로 urlencoding으로 flag을 우회할 수 있다는 것을 알 수 있다.