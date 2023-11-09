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

jumps = [int(line) for line in read_lines(5)]
i=0
pos=0
while True:
    i+=1
    offset=jumps[pos]
    next_pos=pos+offset
    if next_pos >= len(jumps):
        break
    jumps[pos]+=1
    pos=next_pos


part1 = i
print("Part 1:", part1)

jumps = [int(line) for line in read_lines(5)]
i=0
pos=0
while True:
    i+=1
    offset=jumps[pos]
    next_pos=pos+offset
    if next_pos >= len(jumps):
        break
    if offset>=3:
        jumps[pos]-=1
    else:
        jumps[pos]+=1
    pos=next_pos

part2=i
print("Part 2:", part2)
