key = [
    36, 39, 19, 198, 198, 19, 22, 230, 71, 245, 38, 150, 71, 245, 70, 39, 19, 38, 38, 198, 86, 245, 195, 195, 245, 227, 227, 5
]

for k in key:
    answer = []
    for i in range(0, 300):
        if (i * 16) + (i // 16) == k:
            answer += str(i)
            answer += ' '
    print(answer)