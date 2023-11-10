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

lines = read_lines(22)
R=len(lines)
C=len(lines[0])
grid=defaultdict(lambda:'.')
p=R//2*1j+C//2
d=-1j

for r in range(R):
    for c in range(C):
        if lines[r][c]=='#':
            grid[c+r*1j]="#"

infections=0
for _ in range(10_000):
    if grid[p]=='#':
        d*=1j
        grid[p]='.'
    else:
        infections+=1
        d*=-1j
        grid[p]="#"
    p+=d

part1 = infections
print("Part 1:", part1)


grid=defaultdict(lambda:'.')
p=R//2*1j+C//2
d=-1j
infections=0

for r in range(R):
    for c in range(C):
        if lines[r][c]=='#':
            grid[c+r*1j]="#"

for _ in range(10_000_000):
    if grid[p]=='.':
        d*=-1j
        grid[p]='W'
    elif grid[p]=='W':
        grid[p]='#'
        infections+=1
    elif grid[p]=='#':
        d*=1j
        grid[p]='F'
    elif grid[p]=="F":
        d*=-1
        grid[p]="."
    p+=d


part2 = infections
print("Part 2:", part2)
