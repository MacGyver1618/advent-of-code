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

lines = read_lines(13)
gates=dict()
for line in lines:
    depth,rang=map(int,line.split(": "))
    gates[depth]=rang

severity=0
for d in range(0,max(gates)+1):
    if d in gates:
        r=gates[d]
        caught=d%(2*r-2)==0
        if caught:
            severity+=d*r


part1 = severity
print("Part 1:", part1)

passed=False
delay=0
while not passed:
    severity=0
    caught=False
    for d in range(0,max(gates)+1):
        if caught:
            break
        if d in gates:
            r=gates[d]
            caught|=(d+delay)%(2*r-2)==0
    if not caught:
        passed=True
    else:
        delay+=1

part2=delay
print("Part 2:", part2)
