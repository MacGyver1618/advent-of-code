from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(8)

grid = np.zeros([6,50], dtype=int)

for line in inpt:
    if line.startswith("rect"):
        x,y = to_nums(line.split(" ")[1].split("x"))
        grid[0:y, 0:x] = 1
    else:
        d,i,amt = re.match(r"rotate (row|column) [xy]=(\d+) by (\d+)", line).groups()
        if d == "row":
            row = coll.deque(grid[int(i), :])
            row.rotate(int(amt))
            grid[int(i), :] = row
        else:
            col = coll.deque(grid[:, int(i)])
            col.rotate(int(amt))
            grid[:, int(i)] = col

print("Part 1:", np.sum(grid))

print("Part 2:")
for row in grid:
    print("".join(['#' if x == 1 else ' ' for x in row]))

