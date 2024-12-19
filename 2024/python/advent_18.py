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
grid=Grid([[float("inf")]*71 for _ in range(71)])
start=0,0
end=70,70
for i,line in enumerate(lines):
    r,c=parse_ints(line)
    grid.place((r,c),i)

def neighbors(limit):
    return lambda pos: [tuple(n) for n in grid.neighbors(pos) if grid.float_at(n) > limit]

part1 = len(bfs(start,eq(end),neighbors(1023)))-1
print("Part 1:", part1)

lo=1023
hi=len(lines)-1
while hi > lo:
    mid=(hi+lo)//2
    res=bfs(start,eq(end),neighbors(mid))
    if isinstance(res,set):
        hi=mid-1
        part2=lines[mid]
    else:
        lo=mid+1

print("Part 2:", part2)