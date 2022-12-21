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

inpt = read_lines(25)
east = set()
south = set()
for r, line in enumerate(inpt):
    for c, char in enumerate(line):
        if char == ">":
            east.add((r,c))
        if char == "v":
            south.add((r,c))

R = len(inpt)
C = len(inpt[0])


i = 0
while True:
    lines = []
    for r in range(R):
        line = ""
        for c in range(C):
            if (r,c) in east:
                line += "> "
            elif (r,c) in south:
                line += "v "
            else:
                line += "  "
        lines.append(line)
    print("\n".join(lines))
    print()
    next_east = set()
    next_south = set()
    east_moved = False
    south_moved = False
    for sc in east:
        r,c = sc
        cand = r,(c+1) % C
        if cand in east or cand in south:
            next_east.add(sc)
        else:
            east_moved = True
            next_east.add(cand)
    east = next_east
    for sc in south:
        r,c = sc
        cand = (r+1) % R,c
        if cand in east or cand in south:
            next_south.add(sc)
        else:
            south_moved = True
            next_south.add(cand)
    if (not south_moved) and (not east_moved):
        part1 = i + 1
        break
    south = next_south
    i += 1

print("Part 1:", part1)
print("Part 2:", "All done!")
