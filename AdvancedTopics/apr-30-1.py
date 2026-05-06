# April 30, 2026
# 

nameFile = open("./AdvancedTopics/Data/names.txt", "r")
absenceFile = open("./AdvancedTopics/Data/absence.txt", "r")
greetingFile = open("./AdvancedTopics/greetings.txt", "w")
outputFile = open("./AdvancedTopics/output.txt", "w")
wordsFile = open("./AdvancedTopics/Data/words.txt", "r")
IQFile = open("./AdvancedTopics/Data/smarts.txt", "r")

iq = [list(map(int, ii.split(" "))) for ii in IQFile.readlines()]
words = wordsFile.readlines()
absence = absenceFile.readlines()
names = [first.split(" ")[0] for first in nameFile.readlines()]

for i in names:
    greetingFile.write(f"Hello, {i}!\n")

cnt = 0
for i in absence:
    if int(i.split(",")[1]) > 5:
        outputFile.write(i.split(",")[0] + "\n")
    cnt += int(i.split(",")[1])

print(f"Total absences: {cnt}")

wordCount = []
for i in words:
    wordCount.append(words.count(",")+1)

totalIQ = 0
length = 0
for i in iq:
    print(f"Highest IQ: {max(i)}")
    totalIQ += sum(i)
    length += len(i)

print(f"Average IQ: {totalIQ/length:.2f}")

wordsFile.close()
outputFile.close()
absenceFile.close()
nameFile.close()
greetingFile.close()

