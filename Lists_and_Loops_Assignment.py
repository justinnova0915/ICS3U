# Name: Justin
# Date: April 9, 2026
# ICS3U Loops and Lists Assignment

import random

# ---------------------------------------------------------
# QUESTION 1: HASSAN'S RETIREMENT SAVINGS
# ---------------------------------------------------------

# Initial investment and rates
deposit = 5000.0
total_savings = 0.0
annual_increase_rate = 1.04 # 4% increase
interest_rate = 1.07 # 7% interest

# Calculate savings over 40 years
for year in range(40):
    # Deposit money at the start of the year
    total_savings += deposit
    # Apply 7% interest at the end of the year
    total_savings *= interest_rate
    # Increase the deposit amount for the next year
    deposit *= annual_increase_rate

print(f"Hassan will have ${total_savings:.2f} in 40 years when he retires.")

# ---------------------------------------------------------
# QUESTION 2: AMAZON SHOPPING MENU
# ---------------------------------------------------------

items = ["Fortnite tips and tricks", "Xbox controller charger", "Android collectible robot.", "Cell phone case.", "Selfie stick."]
prices = [15.49, 9.29, 6.49, 11.99, 11.39]
subtotal = 0.0

print("\n--Welcome to www.amazon.ca")
while True:
    # Display menu
    for i in range(len(items)):
        print(f"{i+1}. {items[i]:<30} ${prices[i]:.2f}")
    print("6. Exit")
    
    choice = int(input("What would you like? "))
    
    if choice == 6:
        break
    elif 1 <= choice <= 5:
        subtotal += prices[choice - 1]
    else:
        print("Invalid choice, please try again.")

# Calculate shipping and taxes if items were ordered
if subtotal > 0:
    shipping = 0.0
    # Ask for Prime membership if subtotal is under $35
    is_prime = "n"
    if subtotal < 35.00:
        is_prime = input("Are you Amazon Prime member? [y/n] ? ").lower()
    
    # Free shipping if total >= $35 or Prime member, else $5.50
    if subtotal >= 35.00 or is_prime == "y":
        shipping = 0.00
    else:
        shipping = 5.50
        
    tax = subtotal * 0.13 # 13% tax
    total = subtotal + tax + shipping

    # Display results with exactly 2 decimals
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: (13%) ${tax:.2f}")
    print(f"Shipping: ${shipping:.2f}")
    print(f"Total: ${total:.2f}")
else:
    print("Total: $0.00")

# ---------------------------------------------------------
# QUESTION 3: MULTIPLICATIVE DIGITAL ROOT
# ---------------------------------------------------------

num_str = input("\nEnter a number to find its multiplicative digital root: ")
current_val = num_str

# Repeat until the product is between 0 and 9
while len(str(current_val)) > 1:
    product = 1
    digits_to_multiply = []
    
    for digit in str(current_val):
        product *= int(digit)
        digits_to_multiply.append(digit)
    
    print(f"{'*'.join(digits_to_multiply)}={product}")
    current_val = product

print(f"The multiplicative digital root of {num_str} is {current_val}")

# ---------------------------------------------------------
# QUESTION 4: CANNONBALL PYRAMID
# ---------------------------------------------------------

total_cannonballs = int(input("\nEnter the number of cannonballs: "))
layers = 0
used_cannonballs = 0

# Add layers as long as we have enough cannonballs
while True:
    next_layer_balls = (layers + 1) ** 2 # Square number for each layer
    if used_cannonballs + next_layer_balls <= total_cannonballs:
        layers += 1
        used_cannonballs += next_layer_balls
    else:
        break

leftover = total_cannonballs - used_cannonballs
print(f"You can create {layers} layers and there are {leftover} left over cannonballs.")

# ---------------------------------------------------------
# QUESTION 5: UNIVERSITY ENTRANCE AVERAGE
# ---------------------------------------------------------

marks = []
while True:
    mark = float(input("Enter a mark (or -1 to calculate): "))
    
    if mark == -1:
        # Check for minimum 6 valid marks
        if len(marks) < 6:
            print("You must enter at least 6 valid marks (0-100).")
            continue
        else:
            break
    
    # Validate mark range
    if 0 <= mark <= 100:
        marks.append(mark)
    else:
        print("Invalid mark. Please enter a value between 0 and 100.")

# Sort marks descending and take top 6
marks.sort(reverse=True)
top_six = marks[:6]
average = sum(top_six) / 6

print(f"The average of your top six marks is {average:.2f}")

# ---------------------------------------------------------
# QUESTION 6: NBA TRIVIA QUIZ
# ---------------------------------------------------------

# Provided winners list (2000-2025)
winners = [
    "Lakers", "Lakers", "Lakers", "Spurs", "Pistons", "Spurs", "Heat", 
    "Spurs", "Celtics", "Lakers", "Lakers", "Mavericks", "Heat", "Heat", 
    "Spurs", "Warriors", "Cavaliers", "Warriors", "Warriors", "Raptors", 
    "Lakers", "Bucks", "Warriors", "Nuggets", "Celtics", "Thunder"
]

correct_trivia = 0
asked_years = []

print("\n--- NBA Finals Trivia (2000-2025) ---")

for i in range(5):
    # Pick a random unique year
    while True:
        year_idx = random.randint(0, 25)
        if year_idx not in asked_years:
            asked_years.append(year_idx)
            break
    
    year = 2000 + year_idx
    correct_team = winners[year_idx]
    
    # Generate 3 unique options
    options = [correct_team]
    while len(options) < 3:
        random_team = random.choice(winners)
        if random_team not in options:
            options.append(random_team)
    
    random.shuffle(options) # Mix answer positions
    
    print(f"\nWho won the NBA Finals in {year}?")
    for idx, team in enumerate(options):
        print(f"{idx + 1}. {team}")
        
    choice = int(input("Enter your choice (1-3): "))
    
    if options[choice - 1] == correct_team:
        print("Correct!")
        correct_trivia += 1
    else:
        print(f"Wrong! The answer was {correct_team}.")

# Percentage and final comment
final_pct = (correct_trivia / 5) * 100
print(f"\nYou got {correct_trivia}/5 correct ({final_pct:.0f}%).")

if correct_trivia == 5:
    print("You are an NBA expert!")
elif correct_trivia >= 3:
    print("Nice job! You know your hoops.")
else:
    print("I guess you really don't like basketball.")