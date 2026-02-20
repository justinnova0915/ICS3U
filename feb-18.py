# # Feb 18, 2026
# # If Practive Problems

# # 1.
# popcorn = int(input("How many popcorns? "))
# drink = int(input("How many drinks? "))

# cost = popcorn * 6.50 + drink * 3.00

# if popcorn > 1 and drink > 1:
#     cost *= 0.9
#     cost *= 1.13
# else:
#     cost *= 1.13


# print(f"Your cost is ${cost:.2f}")

# # 2.

# subtotal = float(input("Enter your subtotal: "))
# dist = float(input("Enter the distance of your delivery: "))
# loyal = True if input("Are you a loyal memeber? ") == "yes" else False

# fee = 5 + dist * 1.25

# if subtotal >= 50 or (dist < 2 and loyal == True):
#     fee = 0

# print(f"Your delivery fee is ${fee:.2f}. Your total comes to ${subtotal + fee:.2f}.")

# # 3.

# Q = int(input("Enter the quantity: "))
# teach = True if input("Do you have a teach ID? ") == "yes" else False

# price = Q * 4.5

# if Q >= 20 and teach == True:
#     price *= 0.85
# elif Q >= 10:
#     price *= 0.9

# print(f"Your final price is ${price * 1.13:.2f}")

# # 4.

# hours = float(input("How many hours did you park? "))

# if hours > 24:
#     hours = 24

# total = min(20, 4 + (hours - 1)*2.5)

# print(f"Your total fee is ${total:.2f}")

# 5.
