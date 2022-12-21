from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(5)

vents = []

for line in inpt:
    a,b,c,d = map(int, re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups())
    vents.append((A((a,b)),A((c,d))))

covers = coll.defaultdict(lambda: 0)

for vent in vents:
    (x1,y1),(x2,y2) = vent
    if x1 == x2:
        x = x2
        for y in range(min(y1,y2), max(y1,y2)+1):
            covers[(x,y)] += 1
    if y1 == y2:
        y = y2
        for x in range(min(x1,x2), max(x1,x2)+1):
            covers[(x,y)] += 1


part1 = len([x for (x,y) in covers.items() if y > 1])
print("Part 1:", part1)

covers = coll.defaultdict(lambda: 0)

for vent in vents:
    a,b = vent
    d = np.sign(b-a)
    for point in [a + p*d for p in range(max(abs(b-a))+1)]:
        covers[tuple(point)] += 1

part2 = len([x for (x,y) in covers.items() if y > 1])
print("Part 2:", part2)
