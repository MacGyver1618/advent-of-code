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

lines = read_lines(9)
ignore=False
garbage=False
score=0
total=0
garbage_count=0
for c in lines[0]:
    if ignore:
        ignore=False
        continue
    if c == "!":
        ignore=True
        continue
    if garbage:
        if c == ">":
            garbage=False
        else:
            garbage_count+=1
    else:
        if c=="{":
            score +=1
        elif c=="}":
            total += score
            score -= 1
        elif c=="<":
            garbage=True



part1 = total
print("Part 1:", part1)

part2 = garbage_count
print("Part 2:", part2)
