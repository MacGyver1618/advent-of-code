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

lines = read_lines(23)
graph=defaultdict(set)

for line in lines:
    a,b=line.split("-")
    graph[a]|={b}
    graph[b]|={a}

part1=0
for a,b,c in it.combinations(graph, 3):
    if a in graph[b] and b in graph[c] and c in graph[a]:
        if a[0]=="t" or b[0]=="t" or c[0]=="t":
            part1+=1

print("Part 1:", part1)

cliques = []
def max_cliques(r, p, x):
    if not p and not x:
        cliques.append(r)
        return
    for v in p.copy():
        max_cliques(r | {v}, p & graph[v], x & graph[v])
        p.remove(v)
        x.add(v)

max_cliques(set(), set(graph.keys()), set())
part2 = ",".join(sorted(max(cliques, key=len)))
print("Part 2:", part2)

import networkx as nx

G = nx.Graph()
G.add_edges_from(line.split("-") for line in lines)
print(sum(len(c)==3 and any(n.startswith("t") for n in c) for c in nx.enumerate_all_cliques(G)))
print(",".join(sorted(max(nx.find_cliques(G),key=len))))