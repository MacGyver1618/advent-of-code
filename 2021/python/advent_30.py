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

inpt = read_lines(30)

def valid(s):
    depth = 0
    for c in s:
        if c == ')':
            if depth == 0:
                return False
            else:
                depth -= 1
        if c == '(':
            depth += 1
    return depth == 0

working = True

for line in inpt:
    s, expected = line.split()
    expected = 'true' == expected
    working &= expected == valid(s)

print("Algorithm works" if working else "Algorithm broken")