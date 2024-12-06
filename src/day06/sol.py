from typing import List, Tuple, Set

MOVES = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
ROTATE = {"^": ">", ">": "v", "v": "<", "<": "^"}

def parse(data: List[str]) -> Tuple[tuple, List[List[str]]]:
    grid = [list(row) for row in data]
    return next((i, j, c) for i, row in enumerate(data)
                for j, c in enumerate(row) if c in MOVES), grid

def sim(grid: List[List[str]], state: Tuple[int, int, str]) -> Tuple[int, bool]:
    history = {state}
    while True:
        i, j, d = state
        di, dj = MOVES[d]
        ni, nj = i + di, j + dj

        if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0])):
            return len({(i, j) for i, j, _ in history}), False

        state = (i, j, ROTATE[d]) if grid[ni][nj] == "#" else (ni, nj, d)
        if state in history:
            return len({(i, j) for i, j, _ in history}), True
        history.add(state)


def part_one(data: List[str]) -> int:
    guard, grid = parse(data)
    return sim(grid, guard)[0]

def part_two(data: List[str]) -> int:
    guard, grid = parse(data)

    count = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '.':
                grid[i][j] = '#'
                _, loop = sim(grid, guard)
                count += loop
                grid[i][j] = '.'

    return count