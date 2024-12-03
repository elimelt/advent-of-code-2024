import re
from typing import List
from itertools import chain


def parse_mul(line: str):
    reg = r"mul\(\d+,\d+\)"
    return re.findall(reg, line)


def part_one(data: List[str]) -> int:
    eqns = [mul[4:-1].split(",") for line in data for mul in parse_mul(line)]
    return sum([int(eq[0]) * int(eq[1]) for eq in eqns])


def parse_mul_do_dont(line: str):
    rmul = r"mul\(\d+,\d+\)"
    rdo = r"do\(\)"
    rdont = r"don\'t\(\)"

    res = re.findall(rf"{rmul}|{rdo}|{rdont}", line)
    return res


def part_two(data: List[str]) -> int:
    enabled = True
    res = 0
    for expr in [exp for line in data for exp in parse_mul_do_dont(line)]:
        if expr == "do()":
            enabled = True
        elif expr == "don't()":
            enabled = False
        elif "mul" in expr:
            if enabled:
                eq = expr[4:-1].split(",")
                res += int(eq[0]) * int(eq[1])
    return res
