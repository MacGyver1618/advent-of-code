from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(12)

G = coll.defaultdict(list)

for line in inpt:
    a,b = line.split("-")
    G[a] += [b]
    G[b] += [a]

def solve(p2):
    paths = 0
    Q = coll.deque()
    Q.append(('start', {'start'}, False))

    while Q:
        cur, small, twice = Q.popleft()
        if cur == 'end':
            paths += 1
            continue
        for n in G[cur]:
            if n not in small:
                new_small = set(small)
                if n.lower() == n:
                    new_small.add(n)
                Q.append((n, new_small, twice))
            elif n in small and twice is False and p2 and n not in ['start', 'end']:
                Q.append((n, small, True))
    return paths

print("Part 1:", solve(p2=False))
print("Part 2:", solve(p2=True))
