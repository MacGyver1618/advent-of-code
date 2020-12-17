from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
from numpy import array as A

inpt = A([*map(list, lines(18))])
ymax,xmax = inpt.shape

def evolve(grid):
    nxt = grid.copy()
    for j,row in enumerate(grid):
        for i,char in enumerate(row):
            neighbors = [grid[y][x] for x in range(i-1,i+2) for y in range(j-1,j+2) if 0 <= x < xmax and 0 <= y < ymax and (x,y) != (i,j)].count("#")
            if (char == '#' and 2 <= neighbors <= 3) or (char == '.' and neighbors == 3):
                nxt[j][i] = '#'
            else:
                nxt[j][i] = '.'
    return nxt

grid = inpt

for _ in range(100):
    grid = evolve(grid)

print("Part 1:", np.count_nonzero(grid == '#'))

def evolve2(grid):
    nxt = grid.copy()
    for j,row in enumerate(grid):
        for i,char in enumerate(row):
            neighbors = [grid[y][x] for x in range(i-1,i+2) for y in range(j-1,j+2) if 0 <= x < xmax and 0 <= y < ymax and (x,y) != (i,j)].count("#")
            if (char == '#' and 2 <= neighbors <= 3) or (char == '.' and neighbors == 3):
                nxt[j][i] = '#'
            else:
                nxt[j][i] = '.'
        for i,j in it.product([0,xmax-1],[0,ymax-1]):
            nxt[j][i] = '#'
    return nxt

grid = inpt
for i,j in it.product([0,xmax-1],[0,ymax-1]):
    grid[j][i] = '#'
for _ in range(100):
    grid = evolve2(grid)

print("Part 2:", np.count_nonzero(grid == '#'))
