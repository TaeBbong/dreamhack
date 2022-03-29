password = [67, 111, 109, 112, 97, 114, 51, 95, 116, 104, 101, 95, 99, 104, 52, 114, 97, 99, 116, 51, 114]

answer = 'DH{'
for p in password:
	answer += chr(p)
answer += '}'

print(answer)