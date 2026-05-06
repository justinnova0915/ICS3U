

wordFile = open("./words.txt", "r")

result = []

for i in wordFile.readlines():
    row = []
    for j in i.split(","):
        j = j.strip('\n')
        row.append(len(j))
    result.append(row)

print(result)