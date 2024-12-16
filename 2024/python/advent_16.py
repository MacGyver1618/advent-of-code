from common.advent_lib import *
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

lines = read_lines(16)
grid=Grid(lines)
R = len(lines)
C = len(lines[0])

for r, line in enumerate(lines):
    for c,char in enumerate(line):
        if char=="S":
            start=(r,c,0,1)
        elif char=="E":
            end=(r,c)


def neighbors(pos):
    r,c,dr,dc=pos
    for (dr1,dc1) in [(-1,0),(1,0),(0,-1),(0,1)]:
        if (r,c,dr1,dc1) != pos:
            yield (r,c,dr1,dc1)
        if grid.char_at((r+dr,c+dc)) != "#":
            yield (r+dr,c+dc,dr,dc)

def cost(p1,p2):
    if p1[:2]!=p2[:2]:
        return 1
    return 1000

def score(path):
    return sum(cost(p1,p2) for (p1,p2) in zip(path[:-1],path[1:]))

best_path = dijkstra(start, lambda p: p[:2] == end, neighbors, cost)
part1 = score(best_path)
print("Part 1:", part1)

dist = collections.defaultdict(lambda: float("inf"))
dist[start] = 0
Q = heapdict()
Q[start] = 0
prev = defaultdict(list)

while Q:
    u,_ = Q.popitem()
    if u[:2]==end:
        print(f"got to end from {prev[u]}")
        continue
    for v in neighbors(u):
        alt = dist[u] + cost(u,v)
        if alt < dist[v]:
            dist[v] = alt
            prev[v] = [u]
            Q[v] = alt
        elif alt == dist[v]:
            prev[v]+=[u]

optimal_nodes=bfs(end+(0,1), false, lambda p: prev[p])
part2=len({p[:2] for p in optimal_nodes})
print("Part 2:", part2)
