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

lines = read_lines(6)
ts=[*map(int, lines[0].split()[1:])]
ds=[*map(int, lines[1].split()[1:])]

def wins(t,d):
    D = math.sqrt(t**2 - 4*d)
    x2 = (t+D)//2
    x1 = (t-D)//2
    return int(x2-x1)

part1 = math.prod(wins(ts[i], ds[i]) for i in range(4))
print("Part 1:", part1)

t=int("".join(str(t) for t in ts))
d=int("".join(str(t) for t in ds))

part2 = wins(t,d)
print("Part 2:", part2)
