from collections import defaultdict
import math
from typing import List


def parse(data: List[str]) -> List[int]:
    return list(map(list, data))


def get_antennas(data: List[List[str]]) -> List[tuple]:
    n, m = len(data), len(data[0])
    res = []
    for i in range(n):
        for j in range(m):
            if data[i][j] != ".":
                freq = data[i][j]
                res.append((i, j, freq))
    return res


def get_antinodes_outer(n, m, antennas: List[tuple]) -> set[tuple]:
    k = len(antennas)
    res = set()
    for i in range(k):
        for j in range(i + 1, k):
            x1, y1 = antennas[i]
            x2, y2 = antennas[j]
            dx, dy = x2 - x1, y2 - y1

            anodes = (
                (x1 - dx, y1 - dy),
                (x2 + dx, y2 + dy),
            )

            for x, y in anodes:
                if 0 <= x < n and 0 <= y < m:
                    res.add((x, y))
    return res


def get_antinodes_all(n, m, antennas: List[tuple]) -> set[tuple]:
    k = len(antennas)
    res = set()
    for i in range(k):
        for j in range(i + 1, k):
            x1, y1 = antennas[i]
            x2, y2 = antennas[j]
            dx, dy = x2 - x1, y2 - y1

            gcd = math.gcd(dx, dy)

            dx //= gcd
            dy //= gcd

            x, y = x1, y1
            while 0 <= x < n and 0 <= y < m:
                res.add((x, y))
                x += dx
                y += dy

            x, y = x1, y1
            while 0 <= x < n and 0 <= y < m:
                res.add((x, y))
                x -= dx
                y -= dy
    return res


def antinode_search(data, find: callable) -> int:
    antennas = get_antennas(data)
    freq_map = defaultdict(list)
    n, m = len(data), len(data[0])
    for i, j, freq in antennas:
        freq_map[freq].append((i, j))

    all_antinodes = set()
    for freq, antennas in freq_map.items():
        all_antinodes = all_antinodes.union(find(n, m, antennas))

    return all_antinodes


def part_one(data: List[str]) -> int:
    return len(antinode_search(parse(data), get_antinodes_outer))


def part_two(data: List[str]) -> int:
    return len(antinode_search(parse(data), get_antinodes_all))
