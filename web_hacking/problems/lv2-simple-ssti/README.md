## 코드

```python
@app.errorhandler(404)
def Error404(e):
    template = '''
    <div class="center">
        <h1>Page Not Found.</h1>
        <h3>%s</h3>
    </div>
''' % (request.path)
    return render_template_string(template), 404
```
## 풀이

아주 간단한 SSTI 문제
SSTI는 flask에서 render_template_string()을 쓰면 발생한다.
/404에서 입력창에 404 대신 {{7*7}}을 입력하면 49가 출력되는 것으로 확인할 수 있다.
여기서 {{config}}를 입력하면 app에 설정된 값이 나타나고,
SECRET_KEY에 Flag가 저장되어 있다.