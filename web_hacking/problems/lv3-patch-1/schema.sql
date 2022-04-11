create table users(userid TEXT primary key, password TEXT);
create table memo(idx INTEGER primary key AUTOINCREMENT, userid TEXT, title TEXT, contents TEXT);