# # String Manipulation
# '''
# Strings are a bunch of characters strung togerther.
# Operations on strings are different than operations on numbers (int / float)
# '''
# print(5+7)
# print("5"+"7") # "+" overloaded to concatenation instead of addition
# print("Butter" + "fly")
# print(5*"abc") # You can also overload the "*" operator

# # Escape characters
# '''
# \n - new line
# \t - tab
# \\ - the character \
# \' - the character '
# \" - the character "
# '''

# print("Today\nis\nThursday\nFeb\n5")

# # You can also use \t to make a table
# print(40*'=')
# print("Name\t\tage\taverage")
# print(40*'=')
# print("John\t\t16\t87")
# print(40*'=')
# print("Katherine\t15\t87")

# # When using quotes, make sure that the quotes closing 
# # the string is not used in the string itself
# print("I'll be there")
# print("That's mine")

# String indexing
# lists, string, arrays, etc is zero-indexed
word = "abc"

# len() returns the number of characters in the string
print(len(word))

# Slicing strings
school = "Vincent Massey"

# Gets the first character
print(school[0])
# Gets the sixth character
print(school[5])

# Negative indexes start at the end, incrementing backwards
# Gets the last character
print(school[-1])

# You can also get an interval of characters by using the slice operator
# The range is start inclusive and end exclusive
# [start:end] = start, ... , end-1
print(school[3:6])

# If you don't specify a range, it defaults to the edge of the string
print(school[5:])
print(school[:4])


# Useful string methods

# 1.    .find() finds the index of the FIRST occurence of the string/character,
#       left to right, -1 if not found
print(school.find('n'))

# 2.    .rfind() same thing as .find(), but finds the LAST occurence
print(school.rfind('n'))

# 3.    .count() counts the number of times a certain string/character exists
print(school.count("nce"))

# 4.    .replace() replaces the given first parameter with the second parameter, 
#       NOT inplace
print(school.replace("n", "x"))

# 5.    .lower() lowercases the string
print(school.lower())

# 6.    .upper() uppercases the string
print(school.upper())

# 7.    .capitalize capitalizes the string
print(school.capitalize())