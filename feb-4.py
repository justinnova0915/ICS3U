# # Feb 4, 2026

import math

# # 1. Compute the area of a circle given its radius
# print("The area of the circle is", round(3.14*123**2, 2))

# # 2. Computer area given radius
# rad = float(input("Enter the radius: "))
# area = 3.14*rad**2
# print("The area of the circle with radius", rad, "is", round(area,2),"cm sq.")

# # 3. Currency exchange from CAD to Euro
# rate = 0.6196
# money=float(input("Enter the amount in CAD: "))
# euros = money * rate
# print(f"{money} CAD = {euros} EUR")

# # 4.

# first = input("Enter your first name: ")
# last = input("Enter your last name: ")

# # 3 options to print
# # print(last,",",first, sep="")
# # print(last, first, sep=",")
# print(last + "," + first)

# # 5.

# x1 = int(input("Enter x1: "))
# y1 = int(input("Enter y1: "))


# x2 = int(input("Enter x2: "))
# y2 = int(input("Enter y1: "))

# d = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
# print("The distance is:", math.round(d,2))

# # 6. 
# guests = int(input("Enter number of guests: "))

# slices = 32//guests
# left = 32%guests

# print("Option 1: ", slices, "slices each,", left, "left over")
# print("Option 2: ", 32/guests, "slices each")

# # round() rounds numbers correctly except exactly .5
# math.ceil()