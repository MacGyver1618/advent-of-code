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

lines = read_lines(25)

cs = "=-012"
tot = sum(sum((cs.index(c)-2)*5**i for i,c in enumerate(line[::-1])) for line in lines)
s = ""
while tot > 0:
    d = cs[(tot+2)%5]
    s = d + s
    tot = (tot+2)//5

print("Part 1:", s)
print("Part 2: All done!")
