from typing import List, Set, Tuple, Dict
from collections import defaultdict, deque


def parse(data: List[str]) -> List[List[int]]:
    return [[int(c) for c in line.strip()] for line in data]


def find_pos_with_height(
    height_map: List[List[int]], target: int
) -> List[Tuple[int, int]]:
    positions = []
    for i in range(len(height_map)):
        for j in range(len(height_map[0])):
            if height_map[i][j] == target:
                positions.append((i, j))
    return positions


def find_neighbors(
    pos: Tuple[int, int], height_map: List[List[int]]
) -> List[Tuple[int, int]]:
    rows, cols = len(height_map), len(height_map[0])
    i, j = pos
    neighbors = []

    directions = (-1, 0), (1, 0), (0, -1), (0, 1)
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            neighbors.append((ni, nj))

    return neighbors


def bfs(
    start: Tuple[int, int], height_map: List[List[int]], all_nines: Set[Tuple[int, int]]
) -> int:
    visited = set()
    reachable_nines = set()

    queue = deque([(start, 0)])
    visited.add(start)

    while queue:
        pos, current_height = queue.popleft()

        if pos in all_nines:
            reachable_nines.add(pos)
            continue

        for next_pos in find_neighbors(pos, height_map):
            if next_pos not in visited:
                next_height = height_map[next_pos[0]][next_pos[1]]
                if next_height == current_height + 1:
                    queue.append((next_pos, next_height))
                    visited.add(next_pos)

    return len(reachable_nines)


def num_paths_to_nine(start: Tuple[int, int], height_map: List[List[int]]) -> int:
    rows, cols = len(height_map), len(height_map[0])

    dp = defaultdict(int)
    dp[start] = 1

    for height in range(10):
        for i in range(rows):
            for j in range(cols):
                if height_map[i][j] == height and dp[(i, j)] > 0:
                    for ni, nj in find_neighbors((i, j), height_map):
                        if height_map[ni][nj] == height + 1:
                            dp[(ni, nj)] += dp[(i, j)]

    total_paths = 0
    for i in range(rows):
        for j in range(cols):
            if height_map[i][j] == 9:
                total_paths += dp[(i, j)]

    return total_paths


def part_one(data: List[str]) -> int:
    height_map = parse(data)
    trailheads = find_pos_with_height(height_map, 0)
    nine_positions = set(find_pos_with_height(height_map, 9))

    total_score = 0
    for trailhead in trailheads:
        score = bfs(trailhead, height_map, nine_positions)
        total_score += score

    return total_score


def part_two(data: List[str]) -> int:
    height_map = parse(data)
    trailheads = find_pos_with_height(height_map, 0)

    total_rating = 0
    for trailhead in trailheads:
        rating = num_paths_to_nine(trailhead, height_map)
        total_rating += rating

    return total_rating


"""
============================================================
🎄 Advent of Code 2023 - Day 10
🕒 Running at: 2024-12-09 22:10:48
============================================================


🎯 Part 1 Results:
+--------+---------+
| Metric |   Value |
+--------+---------+
| Result |     607 |
| Time   | 16.46ms |
| Memory |  48.0KB |
+--------+---------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 13 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.016    0.016 part_one
     235    0.005    0.000    0.015    0.000 bfs
    3687    0.006    0.000    0.008    0.000 find_neighbors
    14898    0.002    0.000    0.002    0.000 {method 'append' of 'list' objects}
     4901    0.001    0.000    0.001    0.000 {method 'add' of 'set' objects}
     7705    0.001    0.000    0.001    0.000 {built-in method builtins.len}
------------------------------------------------------------

🎯 Part 2 Results:
+--------+----------+
| Metric |    Value |
+--------+----------+
| Result |     1384 |
| Time   | 359.42ms |
| Memory |  448.0KB |
+--------+----------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
  ncalls  tottime  percall  cumtime  percall function
       1    0.006    0.006    0.359    0.359 part_two
     235    0.343    0.001    0.353    0.002 count_paths_to_nine
    4294    0.007    0.000    0.010    0.000 find_neighbors
    17095    0.002    0.000    0.002    0.000 {method 'append' of 'list' objects}
     9106    0.001    0.000    0.001    0.000 {built-in method builtins.len}
       1    0.000    0.000    0.000    0.000 parse
       1    0.000    0.000    0.000    0.000 find_pos_with_height
------------------------------------------------------------
"""
