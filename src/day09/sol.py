from typing import List, Tuple
from collections import defaultdict


def parse_input(data: List[str]) -> List[int]:
    assert len(data) == 1
    res = []
    id = 0
    for i, c in enumerate(data[0]):
        if i % 2 == 0:
            res.extend([id] * int(c))
            id += 1
        else:
            res.extend(["."] * int(c))
    return res


def compact_blocks(blocks):
    n = len(blocks)
    l, r = 0, n - 1
    while l < r and l < n and r >= 0:
        if blocks[r] == ".":
            r -= 1
        elif blocks[l] != ".":
            l += 1
        else:
            blocks[l], blocks[r] = blocks[r], blocks[l]
            l += 1
            r -= 1
    return blocks


def checksum_compacted(blocks):
    s = 0
    for i, n in enumerate(blocks):
        try:
            if n == ".":
                continue
            s += i * int(n)
        except:
            print(i, n)
            raise ValueError()
    return s


def find_files(blocks: List[str]) -> List[Tuple[str, int, int]]:
    files = []
    start = None
    current_id = None

    for i, block in enumerate(blocks):
        if block != ".":
            if block != current_id:
                if start is not None:
                    files.append((current_id, start, i - 1))
                start = i
                current_id = block
        elif start is not None:
            files.append((current_id, start, i - 1))
            start = None
            current_id = None

    if start is not None:
        files.append((current_id, start, len(blocks) - 1))

    return sorted(files, key=lambda x: int(x[0]), reverse=True)


def find_free_spaces(blocks: List[str]) -> List[Tuple[int, int]]:
    spaces = []
    start = None

    for i, block in enumerate(blocks):
        if block == ".":
            if start is None:
                start = i
        elif start is not None:
            spaces.append((start, i - 1))
            start = None

    if start is not None:
        spaces.append((start, len(blocks) - 1))

    return spaces


def compact_sweep(blocks: List[str]) -> List[str]:
    result = blocks.copy()

    files = find_files(result)

    for file_id, file_start, file_end in files:
        file_size = file_end - file_start + 1

        free_spaces = find_free_spaces(result)
        valid_spaces = [
            (start, end)
            for start, end in free_spaces
            if end - start + 1 >= file_size and start < file_start
        ]

        if valid_spaces:
            space_start = min(valid_spaces, key=lambda x: x[0])[0]

            for i in range(file_size):
                result[space_start + i] = file_id

            for i in range(file_start, file_end + 1):
                result[i] = "."

    return result


def part_one(data: List[str]) -> int:
    blocks = compact_blocks(parse_input(data))
    return checksum_compacted(blocks)


def part_two(data: List[str]) -> int:
    blocks = compact_sweep(parse_input(data))
    return checksum_compacted(blocks)


"""
============================================================
🎄 Advent of Code 2024 - Day 09
🕒 Running at: 2024-12-08 22:36:34
============================================================


🎯 Part 1 Results:
+--------+---------------+
| Metric |         Value |
+--------+---------------+
| Result | 6390180901651 |
| Time   |       31.18ms |
| Memory |         1.0MB |
+--------+---------------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
  ncalls  tottime  percall  cumtime  percall function
       1    0.000    0.000    0.031    0.031 part_one
       1    0.009    0.009    0.012    0.012 parse_input
       1    0.010    0.010    0.010    0.010 compact_blocks
       1    0.009    0.009    0.009    0.009 checksum_compacted
    19999    0.003    0.000    0.003    0.000 {method 'extend' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {method 'copy' of 'list' objects}
------------------------------------------------------------

🎯 Part 2 Results:
+--------+---------------+
| Metric |         Value |
+--------+---------------+
| Result | 6412390114238 |
| Time   |        52.62s |
| Memory |         3.9MB |
+--------+---------------+

📊 Profile Data (Top 10 functions):
------------------------------------------------------------
   ncalls  tottime  percall  cumtime  percall  function
------------------------------------------------------------
   Ordered by: cumulative time
   List reduced from 15 to 10 due to restriction <10>
  ncalls  tottime  percall  cumtime  percall function
       1    0.001    0.001   52.623   52.623 part_two
       1    2.748    2.748   52.603   52.603 compact_sweep
   10000   44.814    0.004   47.381    0.005 find_free_spaces
 24419131    2.566    0.000    2.566    0.000 {method 'append' of 'list' objects}
     4897    1.665    0.000    2.462    0.001 {built-in method builtins.min}
11890828    0.797    0.000    0.797    0.000 <lambda>
------------------------------------------------------------
"""
