# April 20, 2026
# 2D Lists

import random
import pprint

setudent = ["Jake", 17, ["Math", "English", "CS"], True]

def printGrid(g):
    for i in range(len(g)):
        for j in range(len(g[i])):
            print(g[i][j], end=" ")
        
        print()

def checkWinner(g:list):
    for i in range(len(g)):
        if g[i][0] == g[i][1] == g[i][2] and g[i][0] != 0:
            return g[i][0]
    
    for i in range(3):
        if g[0][i] == g[1][i] == g[2][i] and g[0][i] != 0:
            return g[0][i]
    
    if g[0][0] == g[1][1] == g[2][2] and g[0][0] != 0:
        return g[0][0]
    elif g[0][2] == g[1][1] == g[2][0] and g[0][2] != 0:
        return g[0][2]
    else: 
        return 0

ticBoard = [[random.randint(0, 2) for i in range(3)] for j in range(3)]
printGrid(ticBoard)
print(checkWinner(ticBoard))

nums = [1, 2, 3, 4]
print(sum(nums))