## 코드

```ini
#################################### Security ############################
[security]
# disable creation of admin user on first start of grafana
disable_initial_admin_creation = false

# default admin user, created on startup
admin_user = admin

# default admin password, can be changed before first start of grafana, or in profile settings
admin_password = admin
```

## 풀이

기본 설정값을 그대로 사용하기 때문에 발생한 취약점..
admin/admin으로 로그인하면 끝난다..
