from typing import List
import re

"""
============================================================
🎄 Advent of Code 2024 - Day 13
🕒 Running at: 2024-12-12 22:14:29
============================================================


🎯 Part 1 Results:
+--------+--------+
| Metric |  Value |
+--------+--------+
| Result |  26599 |
| Time   | 3.71ms |
| Memory |   0.0B |
+--------+--------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 57 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.004    0.004 part_one
       1    0.000    0.000    0.004    0.004 solve_machines
     320    0.001    0.000    0.003    0.000 parse_machine
     960    0.000    0.000    0.002    0.000 match
     960    0.000    0.000    0.001    0.000 _compile
       3    0.000    0.000    0.001    0.000 compile
------------------------------------------------------------

🎯 Part 2 Results:
+--------+-----------------+
| Metric |           Value |
+--------+-----------------+
| Result | 106228669504887 |
| Time   |          3.13ms |
| Memory |            0.0B |
+--------+-----------------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 12 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.003    0.003 part_two
       1    0.000    0.000    0.003    0.003 solve_machines
     320    0.001    0.000    0.002    0.000 parse_machine
     960    0.000    0.000    0.001    0.000 match
     960    0.000    0.000    0.000    0.000 _compile
      960    0.000    0.000    0.000    0.000 {method 'match' of 're.Pattern' objects}
------------------------------------------------------------
"""

def parse_machine(lines: List[str]):
    patterns = [
        r"Button A: X\+(\d+), Y\+(\d+)",
        r"Button B: X\+(\d+), Y\+(\d+)",
        r"Prize: X=(\d+), Y=(\d+)",
    ]

    matches = [re.match(pattern, line) for pattern, line in zip(patterns, lines)]
    points = [(int(match.group(1)), int(match.group(2))) for match in matches]

    return tuple(points)


def find(u, v, t) -> int:
    det = u[0] * v[1] - u[1] * v[0]

    # lin dep? no solution
    if det == 0:
        return -1

    # solve xu + yv = t with cramer rule
    x = (t[0] * v[1] - v[0] * t[1]) / det
    y = (u[0] * t[1] - t[0] * u[1]) / det

    if x != int(x) or y != int(y) or x < 0 or y < 0:
        return -1

    x, y = int(x), int(y)

    return 3 * x + y


def solve_machines(data, offset = 0) -> int:
    ans = 0

    for i in range(0, len(data), 4):
        if i + 3 > len(data):
            break

        a, b, prize = parse_machine(data[i : i + 3])

        if offset:
            prize = (prize[0] + offset, prize[1] + offset)

        tokens = find(a, b, prize)

        if tokens != -1:
            ans += tokens

    return ans


def part_one(data: List[str]) -> int:
    return solve_machines(data)


def part_two(data: List[str]) -> int:
    return solve_machines(data, offset=10000000000000)
