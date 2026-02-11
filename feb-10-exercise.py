# Feb 10, 2026
# If statement practice

# 1.

cost = float(input("Enter the cost of the meal: "))

if cost < 4:
    print("There is no tax!")
    print(f"Your total is ${cost:0.2f}")
else:
    print(f"Your total cost is ${cost * 1.13:0.2f}")
    print(f"Your tax is ${cost*0.13:0.2f}")

# 2.

file = input("Enter the file name: ")
extensions = file[file.rfind('.')+1:]

if extensions == "conf":
    type = "Config file"
elif extensions == "json":
    type = "JSON file"
elif extensions == "gitignore":
    type = "Git ignore file"
elif extensions == ".hpp":
    type = "C++ header file"
elif extensions == "go":
    type = "GO source code"
else:
    type = "Unknown file"

print(f"Your file {file} is a {type}!")

# 3.

temp = float(input("Enter the current temperature: "))

if temp > 20:
    print("T-shirt weather!")
elif 11 <= temp <= 20:
    print("A sweater should be fine.")
elif 0 <= temp <= 10:
    print("Wear a jacket.")
else:
    print("it's freezing — wear a winter coat!")

# 4.
total = float(input("Enter your total amount: "))


if total >= 100:
    saving = total * 0.2
elif total >= 50:
    saving = total * 0.1
else:
    saving = 0

print(f"You have saved ${saving:0.2f}!")
print(f"You have to pay ${total - saving:0.2f}")

# 5.
sentence = input("Enter your sentence: ")
sentence = sentence.lower()

if sentence.find("heck") or sentence.find("darn") or sentence.find("stupid"):
    print("Inappropriate language detected.")
else:
    print("Sentence is clean.")

# 6.
length = float(input("Enter the length of the python: "))

if length > 6:
    area = 6 * 0.5 + (length - 6) * 0.75
else:
    area = length * 0.5

print(f"The area is {area} square feet")