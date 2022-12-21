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

line = read_lines(6)[0]

def solve(l):
    for i in range(len(line)):
        tok = line[i:i+l]
        if len(set(tok)) == l:
            return i+l

print("Part 1:", solve(4))
print("Part 2:", solve(14))
