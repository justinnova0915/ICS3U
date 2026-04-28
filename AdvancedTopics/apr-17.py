# Feb 6, 2026
# Function excersizes
# pdfs/Exercises-functions 2026.pdf

# 5
def knightMoves(row, col):
    moves = [
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (-2, -1),
        (-2, 1),
        (2, -1),
        (2, 1)
    ]

    validMoves = []

    for x, y in moves:
        if 1 <= row+x <= 8 and 1 <= col+y <= 8:
            validMoves.append((row+x, col+y))
        
    return validMoves

print(knightMoves(6, 7))