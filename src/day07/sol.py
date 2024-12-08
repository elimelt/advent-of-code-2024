from typing import List
from typing import Callable

PLUS = lambda x, y: x + y
MULT = lambda x, y: x * y
CONCAT = lambda x, y: int(str(x) + str(y))

OPERATORS_PART_1 = {PLUS, MULT}
OPERATORS_PART_2 = {CONCAT}.union(OPERATORS_PART_1)


def parse(data: List[str]) -> List[tuple[int, List[int]]]:
    result = []
    for line in data:
        target, operands = line.split(":")
        result.append((int(target), list(map(int, operands.strip().split()))))
    return result


def test(
    operators: set[Callable], operands: List[int], i: int, n: int, target: int
) -> bool:

    if n == target and i == len(operands):
        return True
    if i >= len(operands) or n > target:
        return False

    return any(
        test(operators, operands, i + 1, op(n, operands[i]), target) for op in operators
    )


def part_one(data: List[str]) -> int:
    data = parse(data)
    result = []

    for target, operands in data:
        if test(OPERATORS_PART_1, operands, 1, operands[0], target):
            result.append(target)

    return sum(result)


def part_two(data: List[str]) -> int:
    data = parse(data)
    result = []

    for target, operands in data:
        if test(OPERATORS_PART_2, operands, 1, operands[0], target):
            result.append(target)

    return sum(result)
