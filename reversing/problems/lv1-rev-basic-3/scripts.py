key = [
    73, 96, 103, 116, 99, 103, 66, 102, 128, 120, 105, 105, 123, 153, 109, 136, 104, 148, 159, 141, 77, 165, 157, 69
]

flag = ''

for i in range(0, 24):
    temp = (key[i] - 2 * i) ^ i
    flag += chr(temp)

print(flag)
