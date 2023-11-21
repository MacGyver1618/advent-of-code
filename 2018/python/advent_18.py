import copy
import time
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

grid=[[c for c in line] for line in lines]
R=len(grid)
C=len(grid[0])

def print_grid():
    ss=[]
    for r in range(R):
        s=""
        for c in range(C):
            s+=grid[r][c]
        ss+=[s]
    print("\n".join(ss))

def evolve(old_grid):
    new_grid=[row.copy() for row in old_grid]
    for r in range(R):
        for c in range(C):
            tile=grid[r][c]
            neighborhood=""
            for dr in -1,0,1:
                for dc in -1,0,1:
                    if (dr,dc)!=(0,0) and 0<=r+dr<R and 0<=c+dc<C:
                        neighborhood+=old_grid[r+dr][c+dc]
            if tile=='.':
                new_grid[r][c]="|" if neighborhood.count("|")>=3 else "."
            elif tile=="|":
                new_grid[r][c]="#" if neighborhood.count("#")>=3 else "|"
            elif tile=="#":
                new_grid[r][c]="#" if neighborhood.count("#")>=1 and neighborhood.count("|")>=1 else "."

    return new_grid

history=[copy.deepcopy(grid)]
# print_grid()
# input()
while True:
    grid = evolve(grid)
    if grid in history:
        break
    history.append(grid)
    # print_grid()
    # input()
    # time.sleep(.1)

all_tiles=[item for sublist in history[10] for item in sublist]
part1 = all_tiles.count("|")*all_tiles.count("#")
print("Part 1:", part1)

cycle_length=len(history)-history.index(grid)
tail_length=len(history)-cycle_length
generation=(1_000_000_000-tail_length)%cycle_length+tail_length
all_tiles=[item for sublist in history[generation] for item in sublist]
part2 = all_tiles.count("|")*all_tiles.count("#")
print("Part 2:", part2)
