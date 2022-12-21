from common.advent_lib import *
from collections import deque, defaultdict, Counter
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(20)

alg = inpt[0]
grid = defaultdict(lambda: ".")

for y, line in enumerate(inpt[2:]):
    for x, c in enumerate(line):
        if c == "#":
            grid[(x,y)] = c


X = len(inpt[2])
Y = len(inpt[2:])

for i in range(1,51):
    new_grid = defaultdict(lambda: alg[0] if i % 2 == 0 else alg[-1])
    for y in range(-i, Y+i):
        for x in range(-i, X+i):
            s = ""
            for dy in range(-1,2):
                for dx in range(-1,2):
                    s += "1" if grid[(x+dx, y+dy)] == "#" else "0"
            idx = int(s, 2)
            new_grid[(x,y)] = alg[idx]
    grid = new_grid
    if i == 2:
        part1 = len([c for c in grid.values() if c == "#"])

print("Part 1:", part1)

part2 = len([x for x in grid.values() if x == "#"])
print("Part 2:", part2)
