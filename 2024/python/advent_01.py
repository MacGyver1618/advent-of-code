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

lines = read_lines(1)
ls,rs=[],[]
for line in lines:
    l,r=parse_ints(line)
    ls+=[l]
    rs+=[r]

part1=sum(abs(l-r) for l,r in zip(sorted(ls),sorted(rs)))
print("Part 1:", part1)

part2=sum(l*rs.count(l) for l in ls)
print("Part 2:", part2)
