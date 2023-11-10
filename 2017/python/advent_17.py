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

lines = read_lines(17)
spin=int(lines[0])
Q=deque([0])
for i in range(1,50_000_001):
    Q.rotate(-spin)
    Q.append(i)
    if i==2017:
        part1=Q[0]

print("Part 1:", part1)

part2 = Q[Q.index(0)+1]
print("Part 2:", part2)
