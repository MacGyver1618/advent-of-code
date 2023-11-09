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

lines = read_lines(4)
valid=0
valid2=0
for line in lines:
    l=line.split()
    if len(set(l))==len(l):
        valid+=1
    l2=["".join(sorted(w)) for w in l]
    if len(set(l2))==len(l2):
        valid2+=1


part1 = valid
print("Part 1:", part1)

part2 = valid2
print("Part 2:", part2)
