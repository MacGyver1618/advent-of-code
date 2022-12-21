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

lines = read_lines(12)

grid = {}
start = tuple(O)
goal = tuple(O)

for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char == "E":
            goal = (r,c)
            grid[(r,c)] = ord('z')
        elif char == "S":
            start = (r,c)
            grid[(r,c)] = ord('a')
        else:
            grid[(r,c)] = ord(char)

def neighbors(p):
    elev0 = grid[p]
    for cand in map(tuple, adjacent(p)):
        if cand in grid:
            elev = grid[cand]
            if elev0 - elev <= 1:
                yield cand

path = bfs(goal, eq(start), neighbors)
print("Part 1:", len(path)-1)

path = bfs(goal, lambda p: grid[p] == ord('a'), neighbors)
print("Part 2:", len(path)-1)
