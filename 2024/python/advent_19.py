from functools import cache

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

lines = read_lines(19)
patterns=lines[0].split(", ")

@cache
def count_possibles(combo):
    if not combo:
        return 1
    return sum(count_possibles(combo[len(pattern):]) for pattern in patterns if combo.startswith(pattern))

part1 = sum(1 for line in lines[2:] if count_possibles(line)>0)
print("Part 1:", part1)

part2 = sum(count_possibles(line) for line in lines[2:])
print("Part 2:", part2)
