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

inpt = read_lines(3)

def prio(iterables):
    common = first(intersection(iterables))
    if common in abc:
        return ord(common) - ord('a') + 1
    else:
        return ord(common) - ord('A') + 27

print("Part 1:", sum([prio([line[:len(line) // 2], line[:len(line) // 2]]) for line in inpt]))

print("Part 2:", sum([prio([inpt[i], inpt[i + 1], inpt[i + 2]]) for i in range(0, len(inpt), 3)]))
