from collections import defaultdict
from typing import List

"""
============================================================
🎄 Advent of Code 2024 - Day 12
🕒 Running at: 2024-12-11 22:36:57
============================================================


🎯 Part 1 Results:
+--------+---------+
| Metric |   Value |
+--------+---------+
| Result | 1483212 |
| Time   | 89.87ms |
| Memory | 384.0KB |
+--------+---------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.090    0.090 part_one
       1    0.000    0.000    0.090    0.090 solve
        1    0.002    0.002    0.089    0.089 {built-in method builtins.sum}
   19601    0.010    0.000    0.087    0.000 <genexpr>
98000/19600    0.061    0.000    0.076    0.000 dfs_area_perimeter
   195442    0.015    0.000    0.015    0.000 {built-in method builtins.len}
   19600    0.002    0.000    0.002    0.000 <lambda>
------------------------------------------------------------

🎯 Part 2 Results:
+--------+----------+
| Metric |    Value |
+--------+----------+
| Result |   897062 |
| Time   | 164.89ms |
| Memory |  464.0KB |
+--------+----------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 16 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.165    0.165 part_two
       1    0.000    0.000    0.165    0.165 solve
        1    0.003    0.003    0.164    0.164 {built-in method builtins.sum}
   19601    0.011    0.000    0.162    0.000 <genexpr>
   19600    0.110    0.000    0.150    0.000 count_straight_sides
   173960    0.015    0.000    0.015    0.000 {built-in method builtins.len}
------------------------------------------------------------

"""

DIRECTIONS = (0, 1), (1, 0), (0, -1), (-1, 0)


def parse(data: List[str]) -> List[str]:
    return [[c for c in line] for line in data]


def solve(data: List[str], f) -> List[int]:
    data, n, m, ans = parse(data), len(data), len(data[0]), 0
    vis = [[False] * m for _ in range(n)]

    return sum(
        (lambda v: v[0] * v[1])(f(data, data[i][j], i, j, vis))
        for i in range(n)
        for j in range(m)
    )


def dfs_area_perimeter(grid, c, x, y, vis):
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or not grid[x][y] == c:
        return 1, 0

    if vis[x][y]:
        return 0, 0

    vis[x][y] = True

    p, a = 0, 1

    for dx, dy in DIRECTIONS:
        p_, a_ = dfs_area_perimeter(grid, c, x + dx, y + dy, vis)
        p += p_
        a += a_

    return p, a


def part_one(data: List[str]) -> int:
    return solve(data, dfs_area_perimeter)


def find(parent, x):
    if x not in parent:
        parent[x] = x
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]


def union(parent, x, y):
    parent[find(parent, y)] = find(parent, x)


def count_straight_sides(grid, c, x, y, vis):
    if vis[x][y]:
        return 0, 0
    s, vis[x][y], area, sides = [(x, y)], True, 0, set()

    while s:
        cx, cy = s.pop()
        area += 1

        for d, (dx, dy) in enumerate(DIRECTIONS):
            nx, ny = cx + dx, cy + dy

            if (
                nx < 0
                or nx >= len(grid)
                or ny < 0
                or ny >= len(grid[0])
                or grid[nx][ny] != c
            ):
                sides.add((cx, cy, d))
            elif not vis[nx][ny]:
                s.append((nx, ny))
                vis[nx][ny] = True

    parent = {}
    sides = list(sides)

    for i in range(len(sides)):
        for j in range(i + 1, len(sides)):
            x1, y1, d1 = sides[i]
            x2, y2, d2 = sides[j]

            if d1 == d2 and (
                (d1 % 2 == 1 and x1 == x2 and abs(y1 - y2) == 1)
                or (d1 % 2 == 0 and y1 == y2 and abs(x1 - x2) == 1)
            ):
                union(parent, sides[i], sides[j])

    unique_sides = {find(parent, side) for side in sides}
    return len(unique_sides), area


def part_two(data: List[str]) -> int:
    return solve(data, count_straight_sides)
