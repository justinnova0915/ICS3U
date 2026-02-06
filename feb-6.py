# Feb 6, 2026
# f-strings (finally)

'''
Introduced in Python 3.6, f-strings are a great new way to 
format strings. They are more eadfable compared
to the old way, more concise, and less prone to errors
'''

name = 'Justin'
name2 = 'Jerry'
year = 2026
num = 78.49874
cost = 73482.973256
val = 7


# Without f-strings
print("My name is", name, ", and the year is", year)

# With f-strings
print(f"My name is {name}, and the year is {year}")

# You can also reserve spaces for variables using f-string
print(f"My name is {name:10}, and the year is {year}")
print(f"My name is {name2:10}, and the year is {year}")

# You can also add leading zeros using f-strings
print(f"James Bond {val:03}")

# normal round cuts off extra zeros behind the decimal
print(round(num, 2))

# You can display exact deciman places, and f-string rounds for you
print(f"Your total is ${num:9.2f}")
print(f"Your total is ${cost:9.2f}")