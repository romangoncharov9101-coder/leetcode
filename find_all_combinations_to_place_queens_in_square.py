import time
import functools

def get_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'{func.__name__} выполнено за {elapsed:.4f} сек.')
        return result
    return wrapper


def solve_n_queens(square_line):
    solutions = []
    cols, diag1, diag2 = set(), set(), set()
    board = [-1] * square_line

    def backtracking(row):
        if row == square_line:
            solutions.append(tuple(board))
            return
        
        for col in range(square_line):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row] = col

            backtracking(row + 1)

            cols.discard(col)
            diag1.discard(row - col)
            diag2.discard(row + col)
            board[row] = -1
        
    backtracking(0)
    return solutions

def transform(combinations, square_line):
    cords = [(r, combinations[r]) for r in range(square_line)]
    def normalize(c):
        mass = [0] * square_line
        for r, col in c: 
            mass[r] = col
        return tuple(mass)
    variants, cors = [], cords
    for _ in range(4):
        variants.append(normalize(cors))
        variants.append(normalize([(r, square_line-1-c) for r, c in cors]))
        cors = [(c, square_line-1-r) for r, c in cors]
    return variants

def unique_comb(square_line):
    seen, unique = set(), []
    for sol in solve_n_queens(square_line):
        if sol in seen:
            continue
        for v in transform(sol, square_line):
            seen.add(v)
        unique.append(sol)
    return unique

def too_cors(sol):
    return [(r, c) for r, c in enumerate(sol)]

def print_board(queens, coordinates) -> None:
    print()
    cords = set(coordinates)
    for r in range(queens):
        line = ''
        for c in range(queens):
            line += 'Х' if (r, c) in cords else '.'
        print(line)

@get_time
def main():
    square_line = int(input('Длина стороны квадрата: '))
    if square_line == 1 or square_line == 2:
        print_board(square_line, [(0, 0)])
        return
    if square_line == 3:
        print_board(square_line, [(0, 0), (1, 2)])
        return
    sols_set = unique_comb(square_line)
    print(f'Всего уникальных комбинаций: {len(sols_set)}')
    for sol in sols_set:
        print_board(square_line, too_cors(sol))

if __name__ == '__main__':
    main()