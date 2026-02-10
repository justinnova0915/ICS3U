# Feb
# If statments

# Ex1 (Basic if)

# Ex2 (More than 2 options)

mark  = int(input("Enter your mark: "))

# Only one Branch will execute

if mark >= 80:
    print("A")
elif mark >= 70:
    print("B")
elif mark >= 60:
    print("C")
elif mark >= 50:
    print("D")
else:
    print("F")

# Ex3 (using if with strings)

date = input("Whenis your bithday? (mm/dd): ")

if date == "02/09":
    print("Happy birthday!")

# Ex4 (branches can have as many lines as you need)

shape = input("Whawt shape? <rectangle, circle, triangle>: ").lower()

if shape =="rectangle":
    length = float(input("Enter the length: "))
    width = float(input("Enter the width: "))
    area = length*width
    print(f"The area is {area} cm sq")
elif shape == "circle":
    radius = float(input("Enter the radius: "))
    area = 3.14 * radius * 2
    print(f"The area is {area} cm sq")
elif shape == "trangle":
    base = float(input("Enter the base: "))
    height = float(input("Enter the height: "))
    area = base*height/2
    print(f"The area is {area} cm sq")
else:
    print("invalid input!")

# Ext 5a (Nested if statements)

age = int(input("How old are you? "))
if age >= 18:
    citizen = input("Are you a citizen (y/n): ")
    if citizen == "y":
        print("You can vote!")
    else:
        print("You must be a Canadian citizen to vote!")
else:
    print("You are too young to vote!")

# Ext 5b (and operator)
age = int(input("How old are you? "))
citizen = input("Are you a citizen (y/n): ")

if age >= 18 and citizen == "y":
    print("You can vote!")
else:
    print("You can't vote!")