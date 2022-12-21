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

lines = read_lines(18)

cubes = [tuple(to_nums(line.split(","))) for line in lines]

graph = defaultdict(set)

deltas = [
    ( 1, 0, 0),
    (-1, 0, 0),
    ( 0, 1, 0),
    ( 0,-1, 0),
    ( 0, 0, 1),
    ( 0, 0,-1)
]

for cube in cubes:
    for delta in deltas:
        neighbor = tuple(A(cube) + A(delta))
        if neighbor in cubes:
            graph[cube].add(neighbor)
            graph[neighbor].add(cube)

part1 = sum((6-len(graph[cube])) for cube in cubes)
print("Part 1:", part1)

xmin = min(x for x,*_ in cubes)
xmax = max(x for x,*_ in cubes)
ymin = min(y for _,y,*_ in cubes)
ymax = max(y for _,y,*_ in cubes)
zmin = min(z for *_,z in cubes)
zmax = max(z for *_,z in cubes)

approaches = defaultdict(set)
def neighbors(node):
    x,y,z = node
    for (dx,dy,dz) in deltas:
        neighbor = (x + dx, y + dy, z + dz)
        if neighbor in cubes:
            approaches[neighbor].add(node)
        elif xmin-1 <= x+dx <= xmax+1 and ymin-1 <= y+dy <= ymax+1 and zmin-1 <= z+dz <= zmax+1:
            yield neighbor


bfs((0, 0, 0), lambda _: False, neighbors)

part2 = sum(len(views) for cube,views in approaches.items())
print("Part 2:", part2)
