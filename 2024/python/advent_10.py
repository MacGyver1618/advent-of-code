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

lines = read_lines(10)
grid=Grid(lines)

def neighbors(p):
    return [tuple(n) for n in grid.neighbors(p) if grid.int_at(n)==grid.int_at(p)+1]

part1=0
part2=0
for p,val in grid.items():
    if int(val)==0:
        part1+=len([p for p in bfs(p, false, neighbors) if grid.int_at(p)==9])
        part2+=len(all_paths(p, lambda p: grid.int_at(p)==9, neighbors))

print("Part 1:", part1)
print("Part 2:", part2)
