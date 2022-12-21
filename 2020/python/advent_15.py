from common.advent_lib import *
import re
import functools as func
import collections as coll
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(15)[0].split(",")

history = [*map(int, inpt)]
for i in range(len(history)+1,2021):
    last = history[-1]
    previous = [i+1 for i,n in enumerate(history) if n == last]
    if len(previous) == 1:
        history.append(0)
    else:
        history.append(previous[-1]-previous[-2])

print("Part 1:", history[-1])

seen = coll.defaultdict(lambda: coll.deque([], maxlen=2))
for i,n in enumerate(history):
    seen[n].append(i+1)

last = history[-1]
for i in range(len(history)+1,30_000_001):
    if len(seen[last]) < 2:
        last = 0
    else:
        last = seen[last][-1] - seen[last][-2]
    seen[last].append(i)

print("Part 2:", last)
