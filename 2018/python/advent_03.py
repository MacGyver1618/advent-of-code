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

fabrics=dict()
grid=defaultdict(int)
for line in lines:
    num,x,y,w,h=map(int,re.findall(r"\d+", line))
    fabrics[num]=(x,y,w,h)
    for r in range(y,y+h):
        for c in range(x,x+w):
            grid[(r,c)]+=1


part1 = sum(1 for v in grid.values() if v>1)
print("Part 1:", part1)

for no,(x,y,w,h) in fabrics.items():
    if all(grid[(r,c)]==1 for r in range(y,y+h) for c in range(x,x+w)):
        part2=no
        break

print("Part 2:", part2)
