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

lines = read_lines(2)

part1 = 0
for line in lines:
    ns = [*map(int,line.split())]
    part1 += max(ns)-min(ns)

print("Part 1:", part1)

part2 = 0
for line in lines:
    ns = [*map(int,line.split())]
    part2 += [a//b for a in ns for b in ns if a > b and a%b==0][0]
print("Part 2:", part2)
