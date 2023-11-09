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

lines = read_lines(7)

weights=dict()
nodes=set()
edges=set()

for line in lines:
    n,w = re.match(r"([a-z]+) \((\d+)\)", line).groups()
    ns = [n for n in re.findall(r"(?<=[>,] )([a-z]+)", line)]
    nodes.add(n)
    weights[n]=int(w)
    for n2 in ns:
        edges.add((n,n2))

part1 = [node for node in nodes if node not in [b for (a,b) in edges]][0]
print("Part 1:", part1)

subtree_weights=defaultdict(int)
Q=deque([n for n in nodes if n not in [a for a,b in edges]])
while Q:
    n = Q.popleft()
    children = [b for a,b in edges if a==n]
    subtree_weights[n] = weights[n] + sum(subtree_weights[c] for c in children)
    parents = [a for a,b in edges if b==n]
    Q += parents

for n in nodes:
    children = [b for a,b in edges if a==n]
    ws = [subtree_weights[c] for c in children]
    if ws and max(ws) != min(ws):
        weight_diff=max(ws)-min(ws)
        heaviest=[c for c in children if subtree_weights[c]==max(ws)][0]
        part2=weights[heaviest]-weight_diff
        break

print("Part 2:", part2)
