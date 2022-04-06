## 풀이

CSP(Content-Secure-Policy)에 대한 개념 문제
규칙을 작성할 수 있는지 확인하는 문제이다.

```python
try:
    a = driver.execute_script('return a()');
except:
    a = 'error'
try:
    b = driver.execute_script('return b()');
except:
    b = 'error'
try:
    c = driver.execute_script('return c()');
except Exception as e:
    c = 'error'
    c = e
try:
    d = driver.execute_script('return $(document)');
except:
    d = 'error'

if a == 'error' and b == 'error' and c == 'c' and d != 'error':
    return FLAG
```

문제 코드를 보면 a, b 함수는 차단하고 c, d는 허용해줘야 한다는 것을 확인했다.

일단 감을 잡기 위해서 script-src 'none'으로 입력해보면
모두 차단되면서 콘솔에 이상한 sha256 해시값이 나타난다.
여기서 이 해시값이 각 실행단위 코드의 해시값이다.
CSP에서는 이를 기반으로 허용해줄 수 있다.

이때 3번째 함수인 c 함수의 해시값은 'sha256-l1OSKODPRVBa1/91J7WfPisrJ6WCxCRnKFzXaOkpsY4=' 이므로,

script-src 'sha256-l1OSKODPRVBa1/91J7WfPisrJ6WCxCRnKFzXaOkpsY4='와 같이 룰을 적용해주면 나머지는 다 차단되고 c 함수만 허용시킬 수 있으며,

또 하나 허용시켜야 하는 jquery 코드의 경우,

script-src https://code.jquery.com/jquery-3.4.1.slim.min.js 와 같이 룰을 적용할 수 있다.

따라서 전체 코드는

script-src 'sha256-l1OSKODPRVBa1/91J7WfPisrJ6WCxCRnKFzXaOkpsY4=' https://code.jquery.com/jquery-3.4.1.slim.min.js

이렇게 된다.