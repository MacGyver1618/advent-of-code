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

lines = read_lines(8)
grid = [to_nums(line) for line in lines]

R = len(lines)
C = len(grid[0])

visibles = set()
# left
for r in range(R):
    tallest = ()
    height = -1
    for c in range(C):
        tree = grid[r][c]
        if tree > height:
            tallest = (r,c)
            height = tree
            visibles.add(tallest)
# right
for r in range(R):
    tallest = ()
    height = -1
    for c in range(C-1,-1,-1):
        tree = grid[r][c]
        if tree > height:
            tallest = (r,c)
            height = tree
            visibles.add(tallest)
# top
for c in range(C):
    tallest = ()
    height = -1
    for r in range(R):
        tree = grid[r][c]
        if tree > height:
            tallest = (r,c)
            height = tree
            visibles.add(tallest)
# bottom
for c in range(C):
    tallest = ()
    height = -1
    for r in range(R-1,-1,-1):
        tree = grid[r][c]
        if tree > height:
            tallest = (r,c)
            height = tree
            visibles.add(tallest)

print("Part 1:", len(visibles))

scenic = 0
for x,y in [(x,y) for x in range(C) for y in range(R)]:
    height = grid[y][x]
    score = 1
    tallest = -1
    visible = 0
    for c in range(x+1, C):
        tree = grid[y][c]
        visible += 1
        if tree >= height:
            break
    score *= visible
    tallest = -1
    visible = 0
    for c in range(x-1, -1,-1):
        tree = grid[y][c]
        visible += 1
        if tree >= height:
            break
    score *= visible
    tallest = -1
    visible = 0
    for r in range(y+1, R):
        tree = grid[r][x]
        visible += 1
        if tree >= height:
            break
    score *= visible
    tallest = -1
    visible = 0
    for r in range(y-1, -1,-1):
        tree = grid[r][x]
        visible += 1
        if tree >= height:
            break
    score *= visible
    if score > scenic:
        scenic = score

print("Part 2:", scenic)

def visible(starts, increment):
    visibles = set()
    for start in starts:
        height = -1
        pos = A(start)
        while (A((0,0)) <= pos).all() and (pos < A((R,C))).all():
            r,c = pos
            tree = grid[r][c]
            if tree > height:
                height = tree
                visibles.add(tuple(pos))
            pos += A(increment)
    return visibles

top = visible(zip(it.repeat(0), range(C)), (1,0))
bottom = visible(zip(it.repeat(R-1), range(C)), (-1,0))
left = visible(zip(range(R), it.repeat(0)), (0,1))
right = visible(zip(range(R), it.repeat(C-1)), (0,-1))
print(len(top | bottom | right | left))
