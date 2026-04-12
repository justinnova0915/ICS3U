# #1
# c = 0

# while True:
#     mark = int(input("Enter your marks: "))

#     if mark == -1:
#         break
#     elif mark >= 90:
#         c += 1

# print(f"You entered {c} marks that is above 90")

# #2
# sum = 0

# for i in range(64):
#     sum += 2**i

# print(sum)

#3

Hockey = 0
Soccer = 0

while True:
    vote = int(input("Enter vote (0 to exit): "))

    if vote == 1:
        Hockey += 1
    elif vote == 2:
        Soccer += 1
    elif vote == 0:
        break

if Hockey > Soccer:
    print(f"Hockey wins with {(Hockey/(Soccer+Hockey))*100:.0f} of the votes.")
    print(f"Soccer wins with {(Hockey/(Soccer+Hockey))*100:.0f} of the votes.")
else:
