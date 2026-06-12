import functools
import time

def find_queens_coordinates(square_line) -> tuple[int, list[tuple]]:
    if square_line == 1 or square_line == 2:
        return 1, [(0, 0)]
    if square_line == 3:
        return 2, [(0, 0), (1, 2)]
    
    cols = set()
    diag1 = set()
    diag2 = set()
    board = [-1] * square_line
    
    def backtracking(row):
        if row == square_line:
            return True
        
        col_range = range(square_line // 2) if row == 0 else range(square_line)
        
        for col in col_range:
            if col in cols or (row + col) in diag1 or (row - col) in diag2:
                continue

            cols.add(col)
            diag1.add(row + col)
            diag2.add(row - col)
            board[row] = col

            backtracking(row + 1)

            cols.remove(col)
            diag1.remove(row + col)
            diag2.remove(row - col)
        return False
            
    backtracking(0)

    coordinates = [(r, board[r]) for r in range(square_line)]
    return square_line, coordinates

def print_board(queens, coordinates) -> None:
    print()
    cords = set(coordinates)
    for r in range(queens):
        line = ''
        for c in range(queens):
            line += 'Q' if (r, c) in cords else '.'
        print(line)

def main():
    square_line = int(input('Длина стороны: '))
    print(*find_queens_coordinates(square_line))
    _, coordinates = find_queens_coordinates(square_line)
    print(coordinates)
    print_board(square_line, coordinates)
    
if __name__ == '__main__':
    main()