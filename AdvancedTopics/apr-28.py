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
tot = 0
while True:
    val = numFile.readline()
    if val == "":
        break
    #print(repr(val))
    tot += int(val)

print(f"the total is {tot}")
numFile.close()

# Ex2: Using read()
numFile = open("./AdvancedTopics/nums.txt", "r")
myText = numFile.read()
print(repr(myText))
numFile.close()

#Ex3: Using readlines()
numFile = open("./AdvancedTopics/nums.txt", "r")
myList = numFile.readlines()
print(myList)
sum = sum([int(num) for num in myList])
print(sum)
numFile.close()

# Ex4: Writing to files

import random

namesFile = open("./AdvancedTopics/players.txt", "r")
tennis = [name.strip('\n') for name in namesFile.readlines()]
print(tennis)
random.shuffle(tennis)
matchFile = open("./AdvancedTopics/matches.txt", "w")

for i in range(0, len(tennis), 2):
    matchFile.write(f"{tennis[i]:18} vs {tennis[i+1]:20}\n")



namesFile.close()
matchFile.close()

# Ex5

'''
Write a program that will ask the user to enter the room number. You will create a text file based on the room number (e.g. user enteres 103 -> 103.txt)

You will read the names form osslt.txt

in the new file you will enter only the names of students writing the test in that room.
At the bottom of the text file display the total number of students in that room.
'''

ossltFile = open("./AdvancedTopics/osslt.txt", "r")
students = ossltFile.readlines()
rooms = [[] for i in range(55)]

for i in range(len(students)):
    first, last, room = students[i].split(",")
    rooms[int(room)-100].append(f"{first}, {last}")

for i, roomNames in enumerate(rooms):
    if len(roomNames) > 0:
        roomFile = open(f"./AdvancedTopics/rooms/{100+i}", "w")

        for roomName in roomNames: 
            roomFile.write(roomName)
            roomFile.write("\n")
        
        roomFile.write(str(len(roomNames)))

roomFile.close()
ossltFile.close()