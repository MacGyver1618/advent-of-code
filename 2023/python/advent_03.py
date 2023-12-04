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

lines = read_lines(3)
R=len(lines)
C=len(lines[0])

total=0
gears=defaultdict(list)
for r,line in enumerate(lines):
    c=0
    while c<C:
        if line[c] in "0123456789":
            numbers=re.findall(r"\d+",line[c:])
            number=numbers[0]
            l=len(number)
            for r1 in r-1,r,r+1:
                for c1 in range(c-1,c+l+1):
                    if 0<=r1<R and 0<=c1<C:
                        char=lines[r1][c1]
                        if char not in ".0123456789":
                            total+=int(number)
                        if char=="*":
                            gears[(r1,c1)]+=[int(number)]
            c+=l
        else:
            c+=1

part1 = total
print("Part 1:", part1)

part2 = sum(g[0]*g[1] for g in gears.values() if len(g)==2)
print("Part 2:", part2)

