# Feb 19, 2026
# Intro to loops

# # Ex1
# x = 0
# while x < 5:
#     print(x)
#     x += 1

# # Ex2a
# name = ""

# while name != "end":
#     name = input("Enter a name <end to exit>: ")
#     if name != "end":
#         print(f"Hello, {name}!")

# # Ex 2b
# while True:
#     name = input("Enter a name <end to exit>: ")
#     if name == "End":
#         break
#     print(f"Hello, {name}!")

# # Ex 3 Enter marks until -1 is entered, 
# # then display the average of all marks (2 decimals)

# count = 0 # to count the number of marks entered
# total = 0 # to calculate the sum of all marks

# while True:
#     mark = int(input("Enter a mark <-1 to stop>: "))
#     if mark == -1:
#         break
#     elif 0 <= mark <= 100:
#         count += 1
#         total += mark
#     else:
#         print("Invalid input: Marks cannot be less than 0 or larger than 100!")

# print(f"You entered {count} marks")
# print(f"The total is {total}")
# avg = total/count
# print(f"The average is {avg}")

'''
Two important concepts:
1. Counter (type int)
    Keeps track of the number of times we ran the loop
    usually used to keep track of the number of times an event has occured
    
    To use a counter, follow these steps:
        1. give initial value (e.g. count = 0)
        2. each time en event happenes, increase the counter by one
    
    typically, we use this ocunter in calcuation or we use it to exit the loop

2. Accumulator
    similar to a counter
    instead of increasing the value by 1, we can increase it by any number
'''