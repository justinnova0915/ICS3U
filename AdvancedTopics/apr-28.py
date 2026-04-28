# April 28, 2026
# Reading from text files

'''
There are three basic file methods to read from a file

1. read() - reads the ENTIRE FILE as one big string
2. readline() - reads ONE LINE as a string
3. readlines() - reads the ENTIRE FIELE as LIST OF STRINGS (one string per line)
'''

# Ex1: Using readline (this one is usually used in a loop)

numFile = open("./AdvancedTopics/nums.txt", "r")

while True:
    val = numFile.readline()
    if val == "":
        break
    print(repr(val))