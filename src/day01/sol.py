from typing import List

def part_one(data: List[str]) -> int:
    left, right = zip(*(map(int, line.split()) for line in data))
    return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right)))

def part_two(data: List[str]) -> int:
    left, right = zip(*(map(int, line.split()) for line in data))
    right_counts = {x: right.count(x) for x in set(right)}
    return sum(num * right_counts.get(num, 0) for num in left)