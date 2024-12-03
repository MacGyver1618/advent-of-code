import math

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

lines = read_lines(3)
part1=0
part2=0
do=True
for line in lines:
    m=re.findall(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", line)
    for g in m:
        if g[0].startswith("do("):
            do=True
        elif g[0].startswith("don"):
            do=False
        else:
            _,a,b=g
            mul=int(a)*int(b)
            part1+=mul
            part2+=mul if do else 0

print("Part 1:", part1)
print("Part 2:", part2)
