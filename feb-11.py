# # Feb 11, 2026
# # If statement practice questions

# 1.

# miles = int(input("Enter your miles: "))
# points = int(input("Enter your number of points: "))

# if miles < 0 or points < 0:
#     print("Error")
#     exit()

# if miles < 0:
#     print("Invalid input.")
# elif 0 < miles < 1000:
#     points *= 1
# elif 1000 <= miles < 5000:
#     points *= 1.5
# elif 5000 <= miles < 10000:
#     points *= 2
# else:
#     points *= 3

# print(f"You earned {points} points.")

# # 2. 

# water = float(input("Enter your water comsumtion: "))

# if 0 < water <= 5000:
#     cost = water * 0.005
# elif 5000 <= water < 20000:
#     cost = water * 0.004
# elif 20000 < water:
#     cost = water * 0.003
# else:
#     print("Error")
#     exit()

# print(f"The water costs ${cost:.2f}")

# # 3.

# drink = input("Enter your choice <Coffee, Tea, Latte>: ")

# if drink == "Coffee":
#     print(f"Total is ${2.50 * 1.13:.2f}")
# elif drink == "Tea":
#     print(f"Total is ${2.00 * 1.13:.2f}")
# elif drink == "Latte":
#     print(f"Total is ${3.75 * 1.13:.2f}")
# else:
#     print("Error")

# # 4.
# password = input("Enter your password: ")

# if len(password) >= 8 and (password.find('!') != -1 or password.find('@') != -1 or password.find('#') != -1 or password.find('$') != -1 or password.find('%') != -1 or any(char.isdigit() for char in password)):
#     print("Strong password")
# else:
#     print("Weak password")

# # 5.
# average = float(input("Enter your average: "))
# attendance = float(input("Enter your attendance: "))
# teacher = True if input("Do you have teacher recommendation? ") == "yes" else False


# if average >= 80 and (attendance >= 90 or teacher):
#     print("You can!")
# else:
#     print("You can't")

# 6.

age = int(input("Enter your age: "))
days = int(input("Enter your days: "))
credit = int(input("Enter your credit card or ID number >:) "))

if age >= 18 and 0 < days <= 31:
    print("Booking accepted")
else:
    print("Booking denied")