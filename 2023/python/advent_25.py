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

G=defaultdict(set)
for line in lines:
    a,*bs=re.findall(r"\w{3}",line)
    for b in bs:
        G[a].add(b)
        G[b].add(a)

S = set(G)

count = lambda v: len(G[v]-S)
while sum(map(count,S)) != 3:
    S.remove(max(S,key=count))

part1=(len(S)*len(set(G)-S))
print("Part 1:", part1)

part2 = "All done!"
print("Part 2:", part2)
