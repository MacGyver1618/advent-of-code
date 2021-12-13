from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

fish = to_nums(lines(6)[0].split(","))
counts = [fish.count(i) for i in range(9)]

for i in range(256):
    if i == 80:
        part1 = sum(counts)
    counts = [counts[(i+1) % 9] if i != 6 else counts[0] + counts[7] for i in range(9)]

print("Part 1:", part1)
print("Part 2:", sum(counts))
