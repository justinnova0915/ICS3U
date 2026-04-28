# April 20, 2026
# Function Excersizes
# pdfs/Functions Exercises.pdf

import math

def subtract(A:list, B:list):
    A_set = set(A)
    B_set = set(B)

    inter = A_set.intersection(B_set)
    A_set -= inter

    return list(A_set)

def isPrime(num:int):
    max = math.floor(math.sqrt(num))

    for i in range(2, max+1):
        if float(num/i) == num//i:
            return False
    
    return True

def primes(target:int):
    primes = []

    for i in range(2, target):
        if isPrime(i) == True:
            primes.append(i)

    return primes

print(subtract([1, 2, 3], [2, 3, 4]))
print(primes(15))



