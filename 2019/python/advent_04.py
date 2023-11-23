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

start,end=map(int,lines[0].split("-"))

secure=0
for pw in range(start,end+1):
    pw=f"{pw:6d}"
    dd=re.search(r"(.)\1",pw)
    incr=True
    for i in range(1,6):
        if pw[i]<pw[i-1]:
            incr = False
    if dd and incr:
        secure += 1

part1 = secure
print("Part 1:", part1)

secure=0
for pw in range(start,end+1):
    pw=f"{pw:6d}"
    dd=False
    for i in range(10):
        dd=dd or re.search(f"(?<!{i}){i}{i}(?!{i})",pw)
    incr=True
    for i in range(1,6):
        if pw[i]<pw[i-1]:
            incr = False
    if dd and incr:
        secure += 1
part2=secure
print("Part 2:", part2)
