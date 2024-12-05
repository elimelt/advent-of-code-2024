from typing import List
from collections import defaultdict


def make_graph(data: List[str]) -> dict[str, list[str]]:
    graph = defaultdict(list)
    # indegree = defaultdict(int)
    c = 0
    for line in data:
        c += 1
        if line == "":
            break
        s, t = line.split("|")
        graph[s].append(t)

    return graph, c


def make_orderings(data: List[str], c: int) -> list[list[str]]:
    lines = data[c:]
    return [line.split(",") for line in lines]


def search(graph, path) -> bool:
    indegrees = defaultdict(int)
    ele = set(path)
    for u in graph:
        for v in graph[u]:
            if u in ele and v in ele:
                indegrees[v] += 1

    i = 0
    while ele:
        curr = path[i]
        if indegrees[curr] != 0:
            return False
        ele.remove(curr)
        for v in graph[curr]:
            indegrees[v] -= 1
        i += 1
    return True


def part_one(data: List[str]) -> int:
    graph, c = make_graph(data)
    paths = make_orderings(data, c)

    return sum(
        int(path[len(path) // 2]) if search(graph, path) else 0 for path in paths
    )

def sort(graph, path):
    indegrees = defaultdict(int)
    ele = set(path)
    for u in graph:
        for v in graph[u]:
            if u in ele and v in ele:
                indegrees[v] += 1
    while len(ele) > len(path)//2:
        for e in ele:
            if indegrees[e] == 0:
                ele.remove(e)
                for v in graph[e]:
                    indegrees[v] -= 1
                yield e
                break

def part_two(data: List[str]) -> int:
    graph, c = make_graph(data)

    return sum(
        int(s[-1]) for s in [
            list(sort(graph, path))
                for path in make_orderings(data, c)
                if not search(graph, path)
        ]
    )

