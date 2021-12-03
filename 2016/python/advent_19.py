import math

from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

num_elves = int(lines(19)[0])

as_binary = "{0:b}".format(num_elves)

# Josephus probelm binary trick
print("Part 1:", int(as_binary[1:] + as_binary[0], 2))

elves = coll.deque(range(1, num_elves+1))
elves.rotate(math.ceil(len(elves) / 2))

# Elves are removed in order midpoint, +2, +1, +2, +1 and so on
while len(elves) > 1:
    elves.popleft()
    if len(elves) % 2 == 0:
        elves.rotate(-1)

print("Part 2:", elves[0])
