# # Feb 6, 2026
# # Exercises

import math

# # 1.
# name = input("Enter your full name: ")
# i = name.find(' ')
# first = name[:i]
# last = name[i+1:]

# print(f"{last}, {first}")

# # 2.
# word = input("Enter your word: ")
# new = word[-1] + word[1:-1] + word[0]
# print(new)

# # 3.
# file = input("Enter file name: ")
# extension = file[file.rfind(".")+1:]
# print(extension)

# # 4.
# word = input("Enter your word: ")
# new = word[:len(word)//2].lower() + word[len(word)//2:].upper()
# print(new)

# # 5.
# word = input("Enter your string: ")
# length = int(input("Enter your field length: "))
# print('.'*(length-len(word)) + word)

# # 6.
# word = input("Enter your string: ")
# length = int(input("Enter your field length: "))
# print('.'*(math.floor((length-len(word))/2)) + word + '.'*(math.ceil((length-len(word))/2)))

# # 7.
# sentence = input("Enter your sentence: ")
# sentence = sentence.replace(" ", "\n")
# print(sentence)

# # 8.
# num = int(input("Enter your number: "))
# print(('X'*num + '\n')*num)