from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(11)

grid = {}

for y, line in enumerate(inpt):
    for x, c in enumerate(line):
        grid[(x,y)] = int(c)

flashes = 0

adjacent = [
    ( 1, 1),
    ( 1, 0),
    ( 1,-1),
    ( 0, 1),
    ( 0,-1),
    (-1, 1),
    (-1, 0),
    (-1,-1),
]

for i in range(1, 100000):
    new_grid = coll.defaultdict(lambda: 0)
    flashed = set()
    Q = coll.deque()
    for p in [(x,y) for x in range(10) for y in range(10)]:
        new_val = grid[p] + 1
        new_grid[p] = new_val
        if new_val > 9:
            Q.append(p)
            flashed.add(p)
    while Q:
        cur = Q.popleft()
        for n in [tuple(A(cur) + A(d)) for d in adjacent if (A(cur) + A(d) >= O).all()]:
            new_grid[n] += 1
            if new_grid[n] > 9 and n not in flashed:
                Q.append(n)
                flashed.add(n)
    for p in flashed:
        new_grid[p] = 0
        flashes += 1
    if i == 100:
        part1 = flashes
    if len(flashed) == 100:
        part2 = i
        break
    grid = new_grid

print("Part 1:", part1)
print("Part 2:", part2)
