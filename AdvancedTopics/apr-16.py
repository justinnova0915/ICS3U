# Feb 6, 2026
# functions

def hello():
    print("hello massey")

def hi(name):
    print("hi", name)

def avg(a, b):
    return (a+b)/2

hello()

hi("emma")
hi("jake")
hi("vincent")
print(avg(1, 3))

def average(nums):
    total = sum(nums)
    return total/len(nums)

marks = [97, 91, 76, 88]
ages = [15, 18, 17, 16]

print(average(marks))
print(average(ages))