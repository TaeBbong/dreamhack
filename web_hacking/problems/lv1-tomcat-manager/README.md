## 코드

음 딱히 없음..

## 풀이

갑분 톰캣

실행하면 그냥 빈 화면(드림핵 로고)만 나오고 별 다른 반응은 없다.
문제 파일로 제공된 파일은 Dockerfile, ROOT.war, tomcat-users.xml 파일이 있다.
ROOT.war파일의 경우 압축파일 형태로 된 배포 파일로, tomcat에 war 파일을 올리면 해당 서비스가 배포된다.

(지금와서 보니) Dockerfile에는 힌트가 꽤 숨어 있다.
먼저 /flag를 복사해서 root 디렉토리에 복붙하는 부분이 있고,

```dockerfile
COPY ROOT.war /usr/local/tomcat/webapps/ROOT.war
COPY tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml
```

와 같은 부분을 통해 서버의 경로를 알아낼 수 있다.

그리고 가장 중요한(삽질하게 만든) tomcat-users.xml 파일에는 관리자의 계정 정보가 있는데, 여기서 비밀번호는 가려져있는 것을 볼 수 있다.
보아하니 서버에는 실제 비밀번호가 적힌 tomcat-users.xml이 있을 것이다.
근데 나는 여기서 꽂혀서 password를 brute-force하려 했다.
그렇게 생각한 근거는 원래 tomcat-users.xml 파일에는
<Realm className="org.apache.catalina.realm.LockOutRealm" failureCount="20000" >
와 같이 실패횟수를 제한하기 때문이다. 근데 문제에서는 제한하지 않았음..
그런데 실패를 제한하지 않았기 때문에 brute-force가 가능하지 않을까 싶어 스크립트를 만들어 돌려놨었다..

## 풀이 - 진짜

이게 아니라는 것을 금방 깨닫고,
Path Traversal이 되는지 확인해보니 드림핵 로고 이미지의 주소가
http://host1.dreamhack.games:9117/image.jsp?file=working.png
다음과 같음을 알 수 있었다.
image.jsp 파일은 (알고보니) ROOT.war 파일 안에 있고, 이를 열어보면 ../에 대한 필터링이 없는 것을 알 수 있다.
따라서 http://host1.dreamhack.games:9117/image.jsp?file=../../../../../usr/local/tomat/conf/tomcat-users.xml을 시도할 수 있다. (Dockerfile에 제공된 경로 주소)
이걸 하면 실제 tomcat에 대한 비밀번호를 획득할 수 있고,
http://host1.dreamhack.games:9117/manager에 접속한 다음 tomcat과 비밀번호를 입력하면 관리자로 로그인할 수 있다.

로그인하면 몇가지 메뉴들이 있는데,
이 중에서 Deploy WAR가 있다.
WAR 파일을 올리면 알아서 배포가 된다니!
JSP 파일로 된 웹셸을 압축, WAR로 만들어서 올렸다.
올리고 /WAR이름/파일이름.jsp로 이동하면 내가 만든 웹셸이 나오고,
명령어를 실행시켜서 flag 파일을 열어볼 수 있다.(실행파일이라 그냥 열면 된다.)