from functools import lru_cache, partial
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Iterator

"""
============================================================
🎄 Advent of Code 2024 - Day 11
🕒 Running at: 2024-12-10 23:12:14
============================================================


🎯 Part 1 Results:
+--------+----------+
| Metric |    Value |
+--------+----------+
| Result |   377208 |
| Time   | 166.44ms |
| Memory |  832.0KB |
+--------+----------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 438 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.166    0.166 part_one
       1    0.000    0.000    0.166    0.166 solve_concurrently
       1    0.000    0.000    0.162    0.162 __exit__
       1    0.000    0.000    0.162    0.162 shutdown
     2/1    0.000    0.000    0.162    0.162 join
      2/1    0.000    0.000    0.160    0.160 {method 'join' of '_thread._ThreadHandle' objects}
------------------------------------------------------------

🎯 Part 2 Results:
+--------+-----------------+
| Metric |           Value |
+--------+-----------------+
| Result | 449593028787600 |
| Time   |        491.89ms |
| Memory |          64.0KB |
+--------+-----------------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 293 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.492    0.492 part_two
       1    0.000    0.000    0.492    0.492 solve_concurrently
       1    0.000    0.000    0.491    0.491 __exit__
       1    0.000    0.000    0.491    0.491 shutdown
     2/1    0.000    0.000    0.491    0.491 join
      2/1    0.000    0.000    0.489    0.489 {method 'join' of '_thread._ThreadHandle' objects}
------------------------------------------------------------
"""

def parse(data: List[str]) -> Tuple[str]:
    return tuple(data[0].split())


@lru_cache(maxsize=None)
def blink(num: str, times: int) -> int:
    if times == 0:
        return 1

    num_c = int(num)
    if num_c == 0:
        return blink("1", times - 1)

    num_len = len(num)
    if num_len % 2 == 0:
        mid = num_len // 2
        left = str(int(num[:mid]))
        right = str(int(num[mid:]))
        return blink(left, times - 1) + blink(right, times - 1)

    return blink(str(num_c * 2024), times - 1)


def solve_concurrently(
    data: List[str], iterations: int = 75, workers: int = None
) -> int:
    stones = parse(data)

    process_stone = partial(blink, times=iterations)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = executor.map(process_stone, stones)

    return sum(results)


def part_one(data: List[str], blinks: int = 25) -> int:
    return solve_concurrently(data, blinks)


def part_two(data: List[str], blinks: int = 75) -> int:
    return solve_concurrently(data, blinks)
