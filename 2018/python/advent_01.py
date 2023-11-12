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

lines = to_nums(read_lines(1))

part1 = sum(lines)
print("Part 1:", part1)

i=0
history={0}
current=0
while True:
    current+=int(lines[i])
    if current in history:
        part2=current
        break
    history.add(current)
    i=(i+1)%len(lines)

print("Part 2:", part2)
