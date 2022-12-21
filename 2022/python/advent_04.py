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

inpt = read_lines(4)


part1 = 0
part2 = 0
for line in inpt:
    min1,max1,min2,max2 = map(int, re.split(r"[,-]", line))
    r1 = set(range(min1, max1+1))
    r2 = set(range(min2, max2+1))
    if r2.issuperset(r1) or r1.issuperset(r2):
        part1 +=1
    if r1.intersection(r2):
        part2 += 1


print("Part 1:", part1)
print("Part 2:", part2)

print(min([min(map(int, re.split(r"[,-]", line))) for line in inpt]))