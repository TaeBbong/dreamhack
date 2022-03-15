## SOP(Same Origin Policy)

Same Origin : 프로토콜 (Protocol, Scheme), 포트 (Port), 호스트 (Host)이 모두 동일해야 같은 origin 으로 판단
SOP : Same Origin일 때만 리소스에 접근(읽기)할 수 있도록 제한하는 정책

## CORS

`<img>`, `<style>`, `<script>` 태그는 외부의 리소스(Not Same Origin == Cross Origin)이어도 읽기 가능
이외 host가 다른 경우(cafe.naver.com, blog.naver.com ...)라던지
port가 다른 경우(프론트: 5000, 백: 8080)에도 리소스에 접근할 수 있어야 함

이런 경우에는 Cross Origin이지만 예외적으로 허용을 해줘야 함 => CORS(Cross Origin Resource Sharing)

## CORS 방법

기본적으로 CORS는 HTTP 헤더를 기반으로 Cross Origin간에 리소스 공유를 허락해줌
보내는 쪽에서 헤더에 CORS를 설정해서 보내주면, 받는 쪽에서는 이 헤더에 따라 데이터를 가져갈 수 있도록 함

```js
// Client-Side Code
/*
    XMLHttpRequest 객체를 생성합니다. 
    XMLHttpRequest는 웹 브라우저와 웹 서버 간에 데이터 전송을
    도와주는 객체 입니다. 이를 통해 HTTP 요청을 보낼 수 있습니다.
*/
xhr = new XMLHttpRequest();
/* https://theori.io/whoami 페이지에 POST 요청을 보내도록 합니다. */
xhr.open('POST', 'https://theori.io/whoami');
/* HTTP 요청을 보낼 때, 쿠키 정보도 함께 사용하도록 해줍니다. */
xhr.withCredentials = true;
/* HTTP Body를 JSON 형태로 보낼 것이라고 수신측에 알려줍니다. */
xhr.setRequestHeader('Content-Type', 'application/json');
/* xhr 객체를 통해 HTTP 요청을 실행합니다. */
xhr.send("{'data':'WhoAmI'}");
```

```
// Client->Server 요청 헤더
OPTIONS /whoami HTTP/1.1
Host: theori.io
Connection: keep-alive
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
Origin: https://dreamhack.io
Accept: */*
Referer: https://dreamhack.io/
```

```
// Server->Client 응답 헤더
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://dreamhack.io
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Content-Type
```

위처럼 CORS 상태에서 헤더에 CORS 관련 설정을 하고 요청을 보내면,
먼저 OPTIONS라는 메소드로 서버에 요청을 보냄
이것을 preflight라고 함

여기서 OK가 나와야 브라우저는 다시 실제 POST 요청을 보낼 수 있음

## JSONP 방법(old)

`<script>`는 Cross Origin에 구애받지 않고 요청을 보낼 수 있으므로 이를 활용할 수 있음
콜백함수를 만들어서 요청을 보낼때 callback을 지정하면 해당 함수로 전달 받을 수 있음

```js
<script>
/* myCallback이라는 콜백 함수를 지정합니다. */
function myCallback(data){
    /* 전달받은 인자에서 id를 콘솔에 출력합니다.*/
	console.log(data.id)
}
</script>
<!--
https://theori.io의 스크립트를 로드하는 HTML 코드입니다.
단, callback이라는 이름의 파라미터를 myCallback으로 지정함으로써
수신측에게 myCallback 함수를 사용해 수신받겠다고 알립니다.
-->
<script src='http://theori.io/whoami?callback=myCallback'></script>
```