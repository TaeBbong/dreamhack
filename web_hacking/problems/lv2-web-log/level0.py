not_errors = []
with open("web_hacking/problems/lv2-web-log/access_copy.log", "r") as f:
    for line in f:
        if 'GET /board.php?sort=if(ord(substr((select%20group_concat(username,0x3a,password)' in line:
            if '500' in line:
                not_errors.append(line)

f.close()

with open("web_hacking/problems/lv2-web-log/level1.log", "w") as f:
    for line in not_errors:
        f.write(line)

f.close()

answer = ''

with open("web_hacking/problems/lv2-web-log/level1.log", "r") as f:
    for line in f:
        answer += chr(int(line.split('))=')[1].split(',')[0]))

print(answer)
f.close()