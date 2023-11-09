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

lines = read_lines(6)
banks=[int(bank) for bank in lines[0].split()]
history=[]
while tuple(banks) not in history:
    history += [tuple(banks)]
    i = [i for i,c in enumerate(banks) if c==max(banks)][0]
    redist = banks[i]
    banks[i]=0
    while redist:
        i = (i+1)%len(banks)
        banks[i] += 1
        redist -= 1

part1 = len(history)
print("Part 1:", part1)

part2 = len(history)-history.index(tuple(banks))
print("Part 2:", part2)
