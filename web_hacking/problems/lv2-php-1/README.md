## 코드

```php
<h2>View</h2>
<pre><?php
    $file = $_GET['file']?$_GET['file']:'';
    if(preg_match('/flag|:/i', $file)){
        exit('Permission denied');
    }
    echo file_get_contents($file);
?>
</pre>
```

## 풀이

view 페이지에 가보면 파일을 열어보는 기능이 있다. 이때 주소에 flag라는 이름이 들어가면 필터링 되는 것을 알 수 있다.
이 필터링을 우회하기 위해서 PHP Wrapper 라는 기능을 사용할 수 있다.

PHP Wrapper는 PHP에서 제공되는 Wrapper로, 여기서 Wrapper란 어떤 코드나 데이터를 감싸서 기능을 얹는 또다른 코드이다.
쉽게 말해 코드로 코드/데이터를 감싸서 미리 선언된 동작을 하게 하는 것이다.

[php wrapper](https://opentutorials.org/module/4291/26819)

이 기능을 활용하여 공격을 수행할 수 있다. 배경 지식이 필요했던 문제이다.

http://host1.dreamhack.games:9636/?page=php://filter/convert.base64-encode/resource=/var/www/uploads/flag