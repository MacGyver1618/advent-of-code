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
import fractions as frac

lines=read_lines(8)
grid=Grid(lines)

antennas=defaultdict(list)

for p,char in grid.items():
    if char != ".":
        antennas[char]+=[A(p)]

part1=set()
part2=set()

for poss in antennas.values():
    for a, b in it.combinations(poss, 2):
        d = b-a
        part1|={tuple(p) for p in [a-d,b+d] if grid.in_bounds(p)}
        part2|={tuple(p) for p in [a+i*d for i in range(-100,100)] if grid.in_bounds(p)}
print("Part 1:", len(part1))
print("Part 2:", len(part2))
