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

lines = read_lines(25)
stars={tuple(map(int,line.split(","))) for line in lines}

edges = set()
nodes = set()

for a in stars:
    for b in stars:
        if manhattan_distance(a,b) <= 3:
            edges.add((a,b))
            edges.add((b,a))

visited = set()
constellations=0
while len(visited) < len(stars):
    constellations += 1
    unvisited=[star for star in stars if star not in visited]
    Q=deque(unvisited[:1])
    seen={unvisited[0]}
    while Q:
        cur = Q.popleft()
        for n in [b for a,b in edges if a == cur]:
            if n not in seen:
                seen.add(n)
                Q.append(n)
    visited.update(seen)


part1=constellations
print("Part 1:", part1)

part2 = "All done!"
print("Part 2:", part2)
