# Name: Justin
# Date: February 12, 2026
# ICS3U Selection Assignment

import math

# ---------------------------------------------------------
# QUESTION 1: MASSEY MOVIE THEATER
# ---------------------------------------------------------

# Display the pricing table with horizontal lines
print("Category\t1 ticket\t2 tickets\tVIP")
print('-' * 54)
print("Adult\t\t$12.00\t\t$23.00\t\t$42.00")
print('-' * 54)
print("Senior\t\t$8.00\t\t$15.00\t\t$28.00")
print('-' * 54)
print("Student\t\t$9.00\t\t$17.00\t\t$32.00")

# Variables to store user category and ticket choice
user_cat = input("\nEnter your category (Adult, Senior, Student): ").lower()
ticket_type = input("Enter your ticket type (one ticket, two tickets, VIP): ").lower()

price = 0.0

# Nested selection to determine price based on category and ticket type
if user_cat == "adult":
    if ticket_type == "one ticket": 
        price = 12.00
    elif ticket_type == "two tickets": 
        price = 23.00
    elif ticket_type == "vip": 
        price = 42.00
    else: 
        print("Invalid ticket type.")
elif user_cat == "senior":
    if ticket_type == "one ticket": 
        price = 8.00
    elif ticket_type == "two tickets": 
        price = 15.00
    elif ticket_type == "vip": 
        price = 28.00
    else: 
        print("Invalid ticket type.")
elif user_cat == "student":
    if ticket_type == "one ticket": 
        price = 9.00
    elif ticket_type == "two tickets": 
        price = 17.00
    elif ticket_type == "vip": 
        price = 32.00
    else: 
        print("Invalid ticket type.")
else:
    print("Invalid category.")

# Output price rounded to 2 decimals if input was valid
if price > 0:
    print(f"Your total is: ${price:.2f}")

# ---------------------------------------------------------
# QUESTION 2: TRIVIA PROGRAM
# ---------------------------------------------------------

correct_count = 0 # Variable to track right answers

print("\n--- Welcome to the Massey Trivia ---")

# Question 1
ans1 = input("What is the only U.S. state that can be typed using only the top row of a QWERTY keyboard? ").lower()
if ans1 == "alaska":
    print("Correct!") 
    correct_count += 1
else:
    print("Wrong! The answer was Alaska.")

# Question 2
ans2 = input("What do you call the visible part of the rivet on jean pockets? ").lower()
if ans2 == "burr":
    print("Correct!")
    correct_count += 1
else:
    print("Wrong! It's a burr.")

# Question 3
ans3 = input("In human anatomy, what does the 'hallux' refer to? ").lower()
if ans3 == "big toe":
    print("Correct!")
    correct_count += 1
else:
    print("Wrong! It refers to the big toe.")

# Question 4
ans4 = input("What is the name for the plastic/metal tube on the ends of shoelaces? ").lower()
if ans4 == "aglet":
    print("Correct!")
    correct_count += 1
else:
    print("Wrong! It is an aglet.")

# Question 5
ans5 = input("What is the only planet in our solar system to rotate clockwise? ").lower()
if ans5 == "venus":
    print("Correct!")
    correct_count += 1
else:
    print("Wrong! The answer is Venus.")

# Calculate and display percentage
percentage = (correct_count / 5) * 100
print(f"\nGame Over! You got {correct_count}/5 correct.")
print(f"Your score: {percentage:.0f}%")

# ---------------------------------------------------------
# QUESTION 3: ONTARIO INCOME TAX
# ---------------------------------------------------------

salary = float(input("\nEnter your annual salary: ")) 

# Calculate tax using 2026 progressive brackets
if salary < 0:
    print("Invalid input: salary cannot be negative.")
else:
    tax = 0.0
    if salary <= 53891:
        tax = salary * 0.0505
    elif salary <= 107785:
        tax = (53891 * 0.0505) + (salary - 53891) * 0.0915
    elif salary <= 150000:
        tax = (53891 * 0.0505) + (53894 * 0.0915) + (salary - 107785) * 0.1116
    elif salary <= 220000:
        tax = (53891 * 0.0505) + (53894 * 0.0915) + (42215 * 0.1116) + (salary - 150000) * 0.1216
    else:
        # Final bracket rate is 13.16%
        tax = (53891 * 0.0505) + (53894 * 0.0915) + (42215 * 0.1116) + (70000 * 0.1216) + (salary - 220000) * 0.1316

    print(f"The amount of tax you need to pay is: ${tax:.2f}")

# ---------------------------------------------------------
# QUESTION 4: MASSEY AIRLINES BAGGAGE
# ---------------------------------------------------------

weight = float(input("\nEnter luggage weight (kg): "))
fee = 0.0

# Calculate fee based on weight categories
if weight < 0:
    print("Invalid input: weight cannot be negative.")
else:
    if weight <= 15:
        fee = 20.00 # Up to 15 kg
    elif weight <= 25:
        fee = 35.00 # 15.01 to 25 kg
    else:
        # Over 25 kg: Base $35 + $8 per 5kg (or part thereof)
        extra_weight = weight - 25
        extra_units = math.ceil(extra_weight / 5)
        fee = 35.00 + (extra_units * 8)

    print(f"Your baggage fee is: ${fee:.2f}")