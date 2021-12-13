from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(9)
grid = {}

for y, line in enumerate(inpt):
    for x, c in enumerate(line):
        grid[(x,y)] = int(c)

risk = 0
low_points = set()

def neighbors(p):
    x,y = p
    if (x-1,y) in grid:
        yield (x-1,y)
    if (x+1,y) in grid:
        yield (x+1,y)
    if (x,y-1) in grid:
        yield (x,y-1)
    if (x,y+1) in grid:
        yield (x,y+1)

for (x,y), d in grid.items():
    is_low = True
    for neighbor in neighbors((x,y)):
        is_low = is_low and grid[neighbor] > d
    if is_low:
        low_points.add((x,y))
        risk += 1 + d

print("Part 1:", risk)

part2 = 0
basins = set()

for low_point in low_points:
    basin = {low_point}
    Q = coll.deque()
    Q.append(low_point)
    while Q:
        current = Q.popleft()
        for neighbor in neighbors(current):
            if neighbor not in basin and grid[neighbor] != 9:
                basin.add(neighbor)
                Q.append(neighbor)
    basins.add(frozenset(basin))

part2 = product(list(map(len, sorted(basins, key= len, reverse= True)))[:3])

print("Part 2:", part2)
