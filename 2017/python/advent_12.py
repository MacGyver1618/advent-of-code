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

lines = read_lines(12)

nodes = set()
edges = set()
for line in lines:
    n,ns=line.split(" <-> ")
    n=int(n)
    nodes.add(n)
    ns=[*map(int,ns.split(", "))]
    for n2 in ns:
        edges.add((n,n2))
        edges.add((n2,n))

Q=deque([0])
seen=set([0])
while Q:
    cur=Q.popleft()
    for n in [b for a,b in edges if a==cur]:
        if n not in seen:
            Q.append(n)
            seen.add(n)

print("Part 1:", len(seen))

groups=1
unseen=nodes.difference(seen)
while unseen:
    groups+=1
    next_node=[u for u in unseen][0]
    Q=deque([next_node])
    seen=set(Q)
    while Q:
        cur=Q.popleft()
        for n in [b for a,b in edges if a==cur]:
            if n not in seen:
                Q.append(n)
                seen.add(n)
    unseen.difference_update(seen)

part2=groups
print("Part 2:", part2)
