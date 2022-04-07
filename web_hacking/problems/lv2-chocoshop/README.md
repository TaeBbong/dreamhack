## 코드

```python
@app.route('/coupon/submit')
@get_session()
def coupon_submit(user):
    coupon = request.headers.get('coupon', None)
    if coupon is None:
        raise BadRequest('Missing Coupon')

    try:
        coupon = jwt.decode(coupon, JWT_SECRET, algorithms='HS256')
    except:
        raise BadRequest('Invalid coupon')

    if coupon['expiration'] < int(time()):
        raise BadRequest('Coupon expired!')

    rate_limit_key = f'RATELIMIT:{user["uuid"]}'
    if r.setnx(rate_limit_key, 1):
        r.expire(rate_limit_key, timedelta(seconds=RATE_LIMIT_DELTA))
    else:
        raise BadRequest(f"Rate limit reached!, You can submit the coupon once every {RATE_LIMIT_DELTA} seconds.")


    used_coupon = f'COUPON:{coupon["uuid"]}'
    if r.setnx(used_coupon, 1):
        # success, we don't need to keep it after expiration time
        if user['uuid'] != coupon['user']:
            raise Unauthorized('You cannot submit others\' coupon!')

        r.expire(used_coupon, timedelta(seconds=coupon['expiration'] - int(time())))
        user['money'] += coupon['amount']
        r.setex(f'SESSION:{user["uuid"]}', timedelta(minutes=10), dumps(user))
        return jsonify({'status': 'success'})
    else:
        # double claim, fail
        raise BadRequest('Your coupon is alredy submitted!')


@app.route('/coupon/claim')
@get_session()
def coupon_claim(user):
    if user['coupon_claimed']:
        raise BadRequest('You already claimed the coupon!')

    coupon_uuid = uuid4().hex
    data = {'uuid': coupon_uuid, 'user': user['uuid'], 'amount': 1000, 'expiration': int(time()) + COUPON_EXPIRATION_DELTA}
    uuid = user['uuid']
    user['coupon_claimed'] = True
    coupon = jwt.encode(data, JWT_SECRET, algorithm='HS256').decode('utf-8')
    r.setex(f'SESSION:{uuid}', timedelta(minutes=10), dumps(user))
    return jsonify({'coupon': coupon})
```

## 풀이

쿠폰을 발급받아서 돈을 충전한 다음 flag를 구매하는 문제
인데 쿠폰은 1번에 1장밖에 발급받을 수 없고, 1장에 1000원만 충전된다.
또한 쿠폰은 45초만에 만료되며, 이미 쓴 쿠폰이나 다른 사람 쿠폰은 쓸 수 없다.

이 과정에서 논리적 오류가 있는데,
쿠폰은 45초만에 만료가 되지만 실제로 사용할 수 있는 시간은 45.999999...초까지이다.
왜냐면 쿠폰의 만료 시간을 확인하는 코드에서 

```python
if coupon['expiration'] < int(time()):
    raise BadRequest('Coupon expired!')
```

와 같이 int(time())을 하기 때문이다.
따라서 45 < int(45.999999..) = 45 이므로
Coupon expired를 우회할 수 있다.

이게 취약점이 되는 이유는 Coupon expired를 확인한 다음에 쓴 쿠폰인지 검사하기 때문이며,
두번째로 우회해야 되는 쿠폰 사용 여부 확인의 경우

```python
r.expire(used_coupon, timedelta(seconds=coupon['expiration'] - int(time())))
```

으로 작성되어 있다. 이때 coupon['expiration'] - int(time())는 0이 될 것이다. 왜냐면 coupon['expiration']은 최초에 생성될때

```python
data = {'uuid': coupon_uuid, 'user': user['uuid'], 'amount': 1000, 'expiration': int(time()) + COUPON_EXPIRATION_DELTA}
```

와 같이 마찬가지로 int(time())으로 세팅되었으므로, 
45.99999초에 요청을 보내면 Coupon expired는 통과하지만 실제 redis의 coupon은 만료가 되어 사라졌기 때문에 

```python
if r.setnx(used_coupon, 1):
```

여기를 통과할 수 있게 된다.

따라서 이 짧은 찰나에 쿠폰을 또 사용할 수 있게 된다.
이렇게 두번 충전에 성공하고 flag를 요청하면 된다.

redis 함수에 대한 이해가 부족해서 

```python
if r.setnx(used_coupon, 1):
```

이걸 어떻게 우회한거지 싶었는데(이미 한번 이렇게 기록된 애는 안사라지는 줄 알았음..)
r.expire()를 통해 등록해놓은 값은 time이 0이 되면 알아서 만료되고,(redis 자체 기능)
r.setnx()의 경우 key 값이 앞선 r.expire()를 통해 만료되었으므로 통과할 수 있는 것이었다.