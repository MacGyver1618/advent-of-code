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


part1 = sum(int(line)//3-2 for line in lines)
print("Part 1:", part1)

def fuel(n):
    if n < 0:
        return 0
    return max(n//3-2,0)+fuel(n//3-2)

part2 = sum(fuel(int(line)) for line in lines)
print("Part 2:", part2)
