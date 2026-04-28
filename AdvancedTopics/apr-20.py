# Feb 6, 2026
# List Comprehension
# pdfs/Exercises-functions 2026.pdf

# List comprehension is a way of making a list from another list

names = ["Smith", "Jones", "Lee"]

newList = []

# Old way:
# for n in names:
#     newList.append("Mrs. ", n)

# print(newList)

# New way (inline loops):

newList = ["Mrs. " + n for n in names]
print(newList)

nums = [x*x for x in range(1, 11)]
print(nums)

letters  = [letter for letter in "Vincent" if letter > 'j']
print(letters)

ordered_pairs = [(i, j) for i in range(4) for j in range(5, 8)]
print(ordered_pairs)

#son 😭 I don wanna use this cuh

# List mutabillity

# Lists use REFERENCE initilization, not COPY initilization
cities = ["Windsor", "Tecumseh", "Toronto", "Leamington"]
names = cities
# to Copy init
names = cities.copy()
# or
names = cities[:]

print(cities)
print(names)

cities[1] = "Montral"

print(cities)
print(names)

# lists are mutable, strings are immutable
n1 = "Vincent"
n2 = n1
print(n1, n2)
n1 += "Massey"
print(n1, n2)