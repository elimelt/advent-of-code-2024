from typing import List


def is_safe_sequence(levels: List[int]) -> bool:
    if len(levels) < 2:
        return True

    increasing = levels[1] > levels[0]

    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]

        if abs(diff) < 1 or abs(diff) > 3:
            return False
        if increasing and diff < 0:
            return False
        if not increasing and diff > 0:
            return False

    return True


def part_one(lines: List[str]) -> int:
    safe_count = 0

    for line in lines:
        levels = [int(x) for x in line.strip().split()]
        if is_safe_sequence(levels):
            safe_count += 1

    return safe_count


def is_safe_with_dampener(levels: List[int]) -> bool:
    if is_safe_sequence(levels):
        return True

    for i in range(len(levels)):
        dampened_levels = levels[:i] + levels[i + 1 :]
        if is_safe_sequence(dampened_levels):
            return True

    return False


def part_two(lines: List[str]) -> int:
    safe_count = 0

    for line in lines:
        levels = [int(x) for x in line.strip().split()]
        if is_safe_with_dampener(levels):
            safe_count += 1

    return safe_count
