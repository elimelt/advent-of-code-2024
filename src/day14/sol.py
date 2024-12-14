from typing import List
import re
import os

W, H = 101, 103
DIRS = (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)


def parse(data: List[str]):
    for line in data:
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        yield x, y, vx, vy


def print_grid(data):
    grid = [["." for _ in range(W)] for _ in range(H)]
    for x, y, _, _ in data:
        grid[y][x] = "#"

    for row in grid:
        print("".join(row))


def part_one(data: List[str]) -> int:
    data = list(parse(data))

    for t in range(100):
        for i, (x, y, vx, vy) in enumerate(data):
            x = (x + vx) % W
            y = (y + vy) % H

            data[i] = (x, y, vx, vy)

    def count_first_quadrant(data):
        return sum(1 for x, y, _, _ in data if x < W // 2 and y < H // 2)

    def count_last_quadrant(data):
        return sum(1 for x, y, _, _ in data if x > W // 2 and y > H // 2)

    def count_second_quadrant(data):
        return sum(1 for x, y, _, _ in data if x < W // 2 and y > H // 2)

    def count_third_quadrant(data):
        return sum(1 for x, y, _, _ in data if x > W // 2 and y < H // 2)

    q1 = count_first_quadrant(data)
    q2 = count_second_quadrant(data)
    q3 = count_third_quadrant(data)
    q4 = count_last_quadrant(data)
    print(q1, q2, q3, q4)

    return q1 * q2 * q3 * q4


def print_grid(data, largest_island=None):
    grid = [["." for _ in range(W)] for _ in range(H)]

    for x, y, _, _ in data:
        grid[y][x] = "#"

    if largest_island:
        for x, y in largest_island:
            grid[y][x] = "*"

    for row in grid:
        print("".join(row))


def find_cc(positions):

    pos = {(x, y) for x, y, _, _ in positions}
    visited = set()
    best = set()

    def dfs(x: int, y: int, curr):
        if (x, y) in visited or (x, y) not in pos:
            return

        visited.add((x, y))
        curr.add((x, y))

        for dx, dy in DIRS:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < W and 0 <= new_y < H:
                dfs(new_x, new_y, curr)

    for x, y, _, _ in positions:
        if (x, y) not in visited:
            current_island = set()
            dfs(x, y, current_island)
            if len(current_island) > len(best):
                best = current_island

    return best


def part_two(data: List[str]) -> int:
    data = list(parse(data))
    max_island_size = 0
    best_time = 0

    for t in range(10000):
        for i, (x, y, vx, vy) in enumerate(data):
            x = (x + vx) % W
            y = (y + vy) % H
            data[i] = (x, y, vx, vy)

        largest_island = find_cc(data)

        if len(largest_island) > 200:
            return t + 1

    return best_time
