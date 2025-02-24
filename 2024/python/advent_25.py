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

blocks=full_input(25).strip().split("\n\n")
locks=[]
keys=[]
for block in blocks:
    lines=block.split("\n")
    cols=[sum(1 for r in range(7) if lines[r][c]=="#") for c in range(5)]
    if lines[0]=="#####":
        locks+=[cols]
    else:
        keys+=[cols]

part1=sum(all(lock[i]+key[i]<=7 for i in range(5)) for lock in locks for key in keys)
print("Part 1:", part1)
print("Part 2:", "All Done!")
