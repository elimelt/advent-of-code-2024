from typing import List

XMAS = ["X", "M", "A", "S"]


def to_grid(lines: List[str]) -> List[List[str]]:
    return [list(line) for line in lines]


def check(grid: List[List[str]], x: int, y: int, dx: int, dy: int) -> bool:
    n, m = len(grid), len(grid[0])

    for i in range(len(XMAS)):
        new_x, new_y = x + i * dx, y + i * dy
        if new_x < 0 or new_x >= n or new_y < 0 or new_y >= m:
            return False
        if grid[new_x][new_y] != XMAS[i]:
            return False
    return True


def search(grid: List[List[str]], x: int, y: int) -> int:
    if grid[x][y] != "X":
        return 0

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]

    count = 0
    for dx, dy in directions:
        if check(grid, x, y, dx, dy):
            count += 1
    return count


def part_one(data: List[str]) -> int:
    grid = to_grid(data)
    total = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            total += search(grid, x, y)

    return total


def part_two(data: List[str]) -> int:
    return sum(
        [
            int(
                data[x][y] == "A"
                and (data[x - 1][y - 1], data[x + 1][y + 1]) in (("M", "S"), ("S", "M"))
                and (data[x + 1][y - 1], data[x - 1][y + 1]) in (("M", "S"), ("S", "M"))
            )
            for y in range(1, len(data[0]) - 1)
            for x in range(1, len(data) - 1)
        ]
    )
