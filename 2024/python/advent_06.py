import copy

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

R,C,grid = read_grid(6)

dir_=(-1,0)
guard=(0,0)
for r in range(R):
    for c in range(C):
        if grid[r][c]=='^':
            guard=A((r,c))
            grid[r][c]='.'

startpos=guard.copy()

def in_bounds(p):
    r,c=p
    return 0<=r<R and 0<=c<C

def char_at(p):
    r,c=p
    if not in_bounds(p):
        return '.'
    return grid[r][c]

visited=set()
while in_bounds(guard):
    visited.add(tuple(guard))
    if char_at(guard+dir_) == '#':
        dir_=L_turn@dir_
    else:
        guard+=dir_

part1 = len(visited)
print("Part 1:", part1)

part2=0
pb=ProgressBar(len(visited)-1)
for r,c in visited.difference({tuple(startpos)}):
    pb.update()
    guard=startpos.copy()
    dir_=(-1,0)
    history=set()
    grid[r][c]='#'
    while in_bounds(guard):
        state = tuple([*guard, *dir_])
        if state in history:
            part2+=1
            break
        history.add(state)
        if char_at(guard+dir_) == '#':
            dir_=L_turn@dir_
        else:
            guard+=dir_
    grid[r][c]="."
pb.clear()

print("Part 2:", part2)
