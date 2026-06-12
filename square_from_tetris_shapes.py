import random
import time
import math
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


def _rotations(shape: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    seen, result = set(), []
    current = shape
    for _ in range(4):
        min_r = min(r for r, c in current)
        min_c = min(c for r, c in current)
        norm = tuple(sorted((r - min_r, c - min_c) for r, c in current))
        if norm not in seen:
            seen.add(norm)
            result.append(list(norm))
        current = [(c, -r) for r, c in current]
    return result


_BASE_SHAPES = {
    "I": [(0,0),(0,1),(0,2),(0,3)],
    "O": [(0,0),(0,1),(1,0),(1,1)],
    "S": [(0,1),(0,2),(1,0),(1,1)],
    "Z": [(0,0),(0,1),(1,1),(1,2)],
    "L": [(0,0),(1,0),(2,0),(2,1)],
    "J": [(0,1),(1,1),(2,0),(2,1)],
    "T": [(0,0),(0,1),(0,2),(1,1)],
}

TETROMINOES = {name: _rotations(shape) for name, shape in _BASE_SHAPES.items()}
TETROMINO_NAMES = list(TETROMINOES.keys())

SYMBOLS = {
    "I": "I",
    "O": "O",
    "S": "S",
    "Z": "Z",
    "L": "L",
    "J": "J",
    "T": "T",
}


def main_square_side(n_pieces: int) -> int:
    if n_pieces == 0:
        return 0
    cells = 4 * n_pieces
    side = math.ceil(math.sqrt(cells))
    while side * side < cells:
        side += 1
    return side


def fast_greedy_pack(pieces: list[str], start_side: int) -> tuple[int, list[list[str]]]:
    side = start_side
    while True:
        grid = [[' ' for _ in range(side)] for _ in range(side)]
        queue = list(pieces)
        random.shuffle(queue)
        success = True

        for name in queue:
            placed = False
            for r in range(side):
                if placed:
                    break
                for c in range(side):
                    if placed:
                        break
                    for rotation in TETROMINOES[name]:
                        cells = [(r + dr, c + dc) for dr, dc in rotation]
                        if all(0 <= rr < side and 0 <= cc < side and grid[rr][cc] == ' '
                               for rr, cc in cells):
                            for rr, cc in cells:
                                grid[rr][cc] = SYMBOLS[name]
                            placed = True
                            break
            if not placed:
                success = False

        if success:
            return side, grid
        side += 1


def _render_grid(grid: list[list[str]], side: int, pieces: list[str]) -> None:
    filled = sum(1 for row in grid for cell in row if cell != ' ')
    total = side * side

    print(f"\nРазмер: {side}×{side} = {total} клеток | "
          f"Заполнено: {filled} ({filled / total * 100:.1f}%)")

    border = '+' + '-' * (side * 2 + 1) + '+'
    print(border)
    for row in grid:
        print('| ' + ' '.join(row) + ' |')
    print(border)

@get_time
def draw_share(pieces: list[str]) -> None:
    if not pieces:
        print("Нет фигур для размещения.")
        return
    side = main_square_side(len(pieces))
    used_side, grid = fast_greedy_pack(pieces, side)
    _render_grid(grid, used_side, pieces)


def mode_random() -> list[str]:
    while True:
        raw = input("Введите количество фигур (1-1000): ").strip()
        if raw.isdigit() and 1 <= int(raw):
            n = int(raw)
            break
    pieces = [random.choice(TETROMINO_NAMES) for _ in range(n)]
    print(f"Случайный набор ({n} шт.): {', '.join(pieces)}")
    return pieces


def mode_test() -> list[str]:
    counts: dict[str, int] = {}
    for name in TETROMINO_NAMES:
        while True:
            raw = input(f"  {name}: ").strip()
            if raw.isdigit() and int(raw) >= 0:
                counts[name] = int(raw)
                break
            print("введите целое число >= 0.")

    total = sum(counts.values())
    pieces = [name for name, cnt in counts.items() for _ in range(cnt)]
    summary = '  '.join(f"{n}×{c}" for n, c in counts.items() if c > 0)
    print(f"\nИтого {total} фигур: {summary}")
    return pieces


def main() -> None:
    print("=== Тетромино-упаковщик ===\n")
    while True:
        raw = input("Выберите режим  [rand / test]: ").strip().lower()
        if raw == "rand":
            pieces = mode_random()
        elif raw == "test":
            pieces = mode_test()
        else:
            continue
        draw_share(pieces)

if __name__ == '__main__':
    main()