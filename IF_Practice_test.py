# Feb 16, 2026
# If practice test

minutes = float(input("Enter the amount of minuets: ")) # get the time in minutes
weekday = input("Is it the weekday or weekend? (y,n)") # get if its the weekday or weekend

if minutes < 0:
    print("Invalid input: time cannot be negative!")
else:
    if weekday == "y":
        cost = (minutes // 30 + 1) * 1.25 # integer division then add one to account for the remainder as well
    else:
        cost = (minutes // 60 + 1) * 1.5

    print(f"Your total cost is ${cost:.2f}") # only print the cost if the input is valid

# 2.

# get the three sides
a = float(input("Enter the first side: "))
b = float(input("Enter the second side: "))
c = float(input("Enter the third side: "))

# check for negative sides
if a < 0 or b < 0 or c < 0:
    print("Invalid input: sides cannot be negative!")
else:
    # equilateral
    if a == b == c:
        print("The triangle is equilateral.")
    # isosceles
    elif a == b or b == c or a == c:
        print("The triangle is isosceles.")
    # scalene
    else:
        print("The triangle is scalene.")