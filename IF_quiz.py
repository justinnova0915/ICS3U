# Feb 19, 2026
# If test (Version A)

# 1.

# stores the type of currency, type can be either cad or eur
type = input("Enter the currency that you want to convert <eur, cad>: ")

if type == "cad":

    # Get the amount of money to be converted
    money = float(input("Enter the amount of Canadian Dollar that you want to convert: "))
    
    if (money < 0):
        print("Invalid input: Amount can't negative!")
    else:
        # 1 CAD = 1 EUR/1.61
        converted = money/1.61
        print(f"${money:.2f} cad is €{converted:.2f} eur")
        
elif type == "eur":

    # Get the amount of money to be converted
    money = float(input("Enter the amount of Euro that you want to convert: "))
    
    if (money < 0):
        print("Invalid input: Amount can't negative!")
    else:
        # 1 EUR = 1 CAD * 1.61
        converted = money * 1.61
        print(f"€{money:.2f} eur is ${converted:.2f} cad")

else:
    # invalid input handling
    print("Invalid input: Currency has to be either eur or cad!")

# 2.

# stores the pizza type, s, m, or l
type = input("Enter the size of the pizza <s, m, l>: ")

if type == "s":

    # get the number of additional toppings
    toppings = int(input("How many additional toppings do you want? "))
    
    # set toppings to 5 if toppings is more than 5
    if toppings > 5:
        toppings = 5

    # Handling invalid input
    if toppings < 0:
        print("Error: number of additional toppings can't negative!")
    else:

        # calculates total price
        total = 6 + 0.95*toppings
        total *= 1.13
        print(f"Your total is ${total:.2f}")
    
elif type == "m":

    # get the number of additional toppings
    toppings = int(input("How many additional toppings do you want? "))

    # set toppings to 5 if toppings is more than 5
    if toppings > 5:
        toppings = 5
    
    # Handling invalid input
    if toppings < 0:
        print("Error: number of additional toppings can't negative!")
    else:    
        # calculates total price
        total = 8 + 1.25*toppings
        total *= 1.13
        print(f"Your total is ${total:.2f}")

elif type == "l":

    # get the number of additional toppings
    toppings = int(input("How many additional toppings do you want? "))

    # set toppings to 5 if toppings is more than 5
    if toppings > 5:
        toppings = 5
    
    # Handling invalid input
    if toppings < 0:
        print("Error: number of additional toppings can't negative!")
    else:   
        # calculates total price
        total = 11 + 1.45*toppings
        total *= 1.13
        print(f"Your total is ${total:.2f}")

else:
    # Handling invalid input
    print("Error: size has to be one of s, m, or l!")