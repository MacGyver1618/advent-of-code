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

twos=sum(1 for line in lines if 2 in Counter(line).values())
threes=sum(1 for line in lines if 3 in Counter(line).values())

part1 = twos*threes
print("Part 1:", part1)

for a in lines:
    for b in lines:
        diffs=sum(1 for i in range(len(a)) if a[i]!=b[i])
        if diffs==1:
            part2="".join(a[i] for i in range(len(a)) if a[i]==b[i])
            break

print("Part 2:", part2)
