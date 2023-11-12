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

lines = read_lines(5)

def match(a,b):
    if a.isupper() and a.lower()==b:
        return True
    return a.islower() and a.upper()==b
def reduce(s):
    if len(s)<2:
        return s
    for i in range(1,len(s)):
        if match(s[i],s[i-1]):
            return s[:i-1]+s[i+1:]
    return s
def fully_react(s):
    cur = s
    while True:
        _next = reduce(cur)
        if _next==cur:
            return cur
        cur=_next

part1 = len(fully_react(lines[0]))
print("Part 1:", part1)
min_length=float("inf")
for c in abc:
    candidate=re.sub(f"{c}", "", lines[0], flags=re.IGNORECASE)
    reduced=len(fully_react(candidate))
    if reduced<min_length:
        min_length=reduced
part2=min_length
print("Part 2:", part2)
