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

lines = read_lines(3)

grid = defaultdict(int)

wire1 = lines[0].split(",")
wire2 = lines[1].split(",")
dirs={"R":1,"L":-1,"U":-1j,"D":1j}

pos = 0
dist=0
for segment in wire1:
    d=dirs[segment[0]]
    for _ in range(int(segment[1:])):
        pos+=d
        dist+=1
        grid[pos]+=dist

pos = 0
dist=0
for segment in wire2:
    d=dirs[segment[0]]
    for _ in range(int(segment[1:])):
        pos+=d
        dist+=1j
        grid[pos]+=dist


part1 = min(manhattan_distance((0,0),(int(k.real),int(k.imag))) for k,v in grid.items() if v.imag > 0 and v.real > 0)
print("Part 1:", part1)

part2 = min([int(v.imag+v.real) for k,v in grid.items() if v.real > 0 and v.imag > 0])
print("Part 2:", part2)
