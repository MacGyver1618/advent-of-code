import sys

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

lines = read_lines(14)
grid = [[c for c in line] for line in lines]
R=len(grid)
C=len(grid[0])
rs=[r for r in range(R)]
cs=[c for c in range(C)]

def bubble(r,c,dr,dc):
    while 0 <= r+dr < R and 0 <= c+dc < C and grid[r+dr][c+dc]==".":
        grid[r+dr][c+dc]="O"
        grid[r][c]="."
        r+=dr
        c+=dc

def north():
    for r in rs:
        for c in cs:
            if grid[r][c]=='O':
                bubble(r,c,-1,0)

def south():
    for r in rs[::-1]:
        for c in cs:
            if grid[r][c]=='O':
                bubble(r,c,1,0)

def east():
    for c in cs[::-1]:
        for r in rs:
            if grid[r][c]=='O':
                bubble(r,c,0,1)

def west():
    for c in cs:
        for r in rs:
            if grid[r][c]=='O':
                bubble(r,c,0,-1)

north()

part1 = sum(R-r for r in rs for c in cs if grid[r][c]=="O")
print("Part 1:", part1)

grid = [[c for c in line] for line in lines]

def cycle(_):
    north()
    west()
    south()
    east()
    return [(r,c) for r in rs for c in cs if grid[r][c]=="O"]

state=cycle_until_nth([(r,c) for r in rs for c in cs if grid[r][c]=="O"],cycle,1_000_000_000)
part2=sum(R-r for r,c in state)
print("Part 2:", part2)
