# Name: Justin Li
# Date: May 5, 2026
# ICS3U Files Assignment

import math

# ---------------------------------------------------------
# QUESTION 1: ATP PLAYER RANKING FILTER
# ---------------------------------------------------------

ATPFile = open("./AdvancedTopics/Data/ATP.txt", "r")

# Ask user for the point range
MIN = int(input("Enter the points FROM: "))
MAX = int(input("Enter the points TO: "))
print("-" * 30)

# Load data into a list of lists
ATP = [i.split(",") for i in ATPFile.readlines()]

minIndex = 0
maxIndex = 0

# Find the starting and ending indices based on points
for P in range(len(ATP)):
    if int(ATP[P][-1]) < MAX:
        maxIndex = P + 1
        break

for P in range(len(ATP)):
    if int(ATP[P][-1]) < MIN:
        minIndex = P
        break

# Output total count of players in range
print(f"{minIndex - maxIndex + 1} players total")

# Create output file with name based on point range
minmaxFile = open(f"./AdvancedTopics/{MIN}to{MAX}.txt", "w")

# Write ranking, last name, and points to the file
for j in range(maxIndex, minIndex + 1):
    minmaxFile.write(f"{ATP[j-1][0]},{ATP[j-1][2]},{ATP[j-1][-1]}")

minmaxFile.close()
ATPFile.close()

# ---------------------------------------------------------
# QUESTION 2: PERSONAL STOCK PORTFOLIO
# ---------------------------------------------------------

portfolioFile = open("./AdvancedTopics/Data/myportfolio.txt", "r")
stocksFile = open("./AdvancedTopics/Data/stocks.txt", "r")

# Create dictionary for quick lookup from stocks.txt
# Format: { 'CODE': ['Name', 'Code', 'Price'] }
stocks = {s.split('\t')[1]: s.split('\t') for s in stocksFile.readlines()}
portfolio = [p.split('\t') for p in portfolioFile.readlines()]

print("\nPersonal Stock Portfolio")
print("-" * 40)
print(f"{'Company Name':<18}{'Price':<11}{'Value'}")

totalPortfolio = 0.0

# Process each stock in the personal portfolio
for P in portfolio:
    code = P[0]
    shares = int(P[1])
    
    if code in stocks:
        name = stocks[code][0]
        price = float(stocks[code][2])
        value = price * shares
        totalPortfolio += value
        
        # Display formatted table rows
        print(f"{name:18}{price:<11.2f}{value:<11.2f}")
        print("-" * 40)

# Display total value of the entire portfolio
print(f"Total Portfolio Value: ${totalPortfolio:.2f}")

portfolioFile.close()
stocksFile.close()

# ---------------------------------------------------------
# QUESTION 3: LEBRON JAMES POINTS TRACKER
# ---------------------------------------------------------

lebronFile = open("./AdvancedTopics/Data/lebron.txt", "r")

# Flatten all comma-separated points into a single integer list
all_points = []
for line in lebronFile.readlines():
    quarters = line.strip().split(",")
    for q in quarters:
        if q != "":
            all_points.append(int(q))

gameNum = 1

# Calculate totals for every 4 quarters to represent one game
for i in range(0, len(all_points), 4):
    # Sum the slice of 4 quarters
    gameSum = sum(all_points[i : i+4])
    print(f"Game {gameNum}: {gameSum}")
    gameNum += 1

lebronFile.close()