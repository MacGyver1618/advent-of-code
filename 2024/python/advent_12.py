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
import time

lines = read_lines(12)
grid=Grid(lines)

populated=set()
areas=set()

def neighbors(v):
    def _neighbors(p):
        for n in grid.neighbors(p):
            if grid.char_at(n)==v:
                yield tuple(n)
    return _neighbors

for p,v in grid.items():
        if p not in populated:
            flooded = bfs(p,false,neighbors(v))
            areas.add(frozenset(flooded))
            populated.update(flooded)

part1=0
for area in areas:
    perimeter=sum(len([n for n in adjacent(p) if tuple(n) not in area]) for p in area)
    part1+=len(area)*perimeter

print("Part 1:", part1)

part2=0
for area in areas:
    sides=0
    for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:#L,D,R,U
        visited=set()
        oriented_edges=[(r,c) for (r,c) in sorted(area) if (r+dr,c+dc) not in area]
        for node in oriented_edges:
            r,c=node
            if node in visited:
                continue
            sides+=1
            nr,nc=abs(dc),abs(dr)
            while node in oriented_edges:
                visited.add(node)
                rr,cc=node
                node=rr+nr,cc+nc
    part2+=len(area)*sides

print("Part 2:", part2)
