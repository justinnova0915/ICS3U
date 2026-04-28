# Name: Justin
# Date: April 27, 2026
# Functions Assignment

# ---------------------------------------------------------
# QUESTION 1: COUNT VOWELS
# ---------------------------------------------------------

def count_vowels(word: str):
    # Make the string lowercase so we don't have to check for uppercase vowels individually
    word = word.lower()
    count = 0
    
    # Use the built-in count() method to find all occurrences of each vowel
    # and add them to our running total
    count += word.count("a")
    count += word.count("e")
    count += word.count("i")
    count += word.count("o")
    count += word.count("u")

    return count

# Test the function
print(count_vowels("Justin"))

# ---------------------------------------------------------
# QUESTION 2: BISHOP MOVES
# ---------------------------------------------------------

def bishop_moves(pos: tuple):
    # Initialize an empty list to store the coordinates of all valid moves
    moves = [] 

    # Check every single square on an 8x8 chessboard
    for i in range(1, 9):
        for j in range(1, 9):
            # A square is on the same diagonal if the horizontal distance 
            # equals the vertical distance from the current position
            if abs(pos[0] - i) == abs(pos[1] - j):
                # The piece must move to a new square, so ignore its current position
                if pos != (i, j):
                    moves.append((i, j))
    
    return moves

# Test the function with a starting coordinate
print(bishop_moves((0, 0)))

# ---------------------------------------------------------
# QUESTION 3: CHECKERBOARD
# ---------------------------------------------------------

def generate_checkerboard(w, h):
    board = []

    # Use booleans to act as a toggle switch between 1 and 0
    row_color = True
    color = False
    
    # Loop to create each row of the board
    for i in range(h):
        row = []
        row_color = color # Set the starting number for this specific row
        
        # Loop to fill the current row column by column
        for j in range(w):
            if row_color:
                row.append(1) 
            else:
                row.append(0)

            # Toggle the boolean to alternate the number for the next column
            row_color = not row_color
            
        # Toggle the starting boolean so the next row staggers the pattern
        color = not color

        board.append(row)
    
    return board

# Generate a board with width 8, height 6
checkerboard = generate_checkerboard(8, 6)

# Print the 2D list formatted as a visual grid
print("[", end="")
for i in range(len(checkerboard)):
    if i == 0:
        # The first row sits right next to the opening bracket
        print(f"{checkerboard[i]},")
    elif i == len(checkerboard) - 1:
        # The last row needs an indent to align, and ends with the closing bracket
        print(f" {checkerboard[i]}]")
    else:
        # Middle rows need a single space indent to perfectly align with the first row
        print(f" {checkerboard[i]},")

# ---------------------------------------------------------
# QUESTION 4: CONNECT 4 WIN CHECKER
# ---------------------------------------------------------

def check_connect_4(board):
    rows = 6
    cols = 7

    # Iterate through every single cell on the board to check for a winning sequence
    for r in range(rows):
        for c in range(cols):
            player = board[r][c]
            
            # If the cell is empty, it can't be part of a win, so skip to the next cell
            if player == 0:
                continue

            # Check 4 spaces to the right (Horizontal Win)
            # We first ensure adding 3 to the column doesn't go off the board
            if c + 3 < cols:
                if player == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                    return True

            # Check 4 spaces down (Vertical Win)
            # We ensure adding 3 to the row doesn't go off the bottom of the board
            if r + 3 < rows:
                if player == board[r+1][c] == board[r+2][c] == board[r+3][c]:
                    return True

            # Check 4 spaces diagonally down and to the right
            if r + 3 < rows and c + 3 < cols:
                if player == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                    return True

            # Check 4 spaces diagonally down and to the left
            if r + 3 < rows and c - 3 >= 0:
                if player == board[r+1][c-1] == board[r+2][c-2] == board[r+3][c-3]:
                    return True

    # If the loop finishes checking every cell and finds no matches, there is no winner
    return False

# Create a clean 6x7 board filled with 0s for testing
empty_board = [[0 for _ in range(7)] for _ in range(6)]

print("\n--- Connect 4 Tests ---")

# Test 1: Horizontal win
horiz_win = [row[:] for row in empty_board]
horiz_win[0][0] = horiz_win[0][1] = horiz_win[0][2] = horiz_win[0][3] = 1
print(f"Horizontal Win: {check_connect_4(horiz_win)}") # Expected: True

# Test 2: Vertical win
vert_win = [row[:] for row in empty_board]
vert_win[0][0] = vert_win[1][0] = vert_win[2][0] = vert_win[3][0] = 2
print(f"Vertical Win: {check_connect_4(vert_win)}")   # Expected: True

# Test 3: No win
print(f"Empty Board Win: {check_connect_4(empty_board)}") # Expected: False

# Test 4: Diagonal win (down-right)
diag_win = [row[:] for row in empty_board]
for i in range(4):
    diag_win[i][i] = 1
print(f"Diagonal Win: {check_connect_4(diag_win)}")   # Expected: True