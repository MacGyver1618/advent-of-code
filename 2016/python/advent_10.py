from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(10)

edges = set()
values = coll.defaultdict(list)
nodes = set()

for line in inpt:
    if line.startswith("value"):
        v,b = re.match(r"value (\d+) goes to (bot \d+)", line).groups()
        values[b].append(int(v))
        nodes.add(b)
    else:
        bot,low,high = re.match(r"(bot \d+) gives low to ((?:output|bot) \d+) and high to ((?:output|bot) \d+)", line).groups()
        edges.add((bot, low, 0))
        edges.add((bot, high, 1))
        nodes.update([bot,low,high])


L = []
S = {node for node in nodes if node not in {b for _,b,_ in edges}}
remaining_edges = edges.copy()

while S:
    n = S.pop()
    L.append(n)
    for e in {(a,b,c) for a,b,c in remaining_edges if a == n}:
        _,m,_ = e
        remaining_edges.remove(e)
        if not {_ for a,b,_ in remaining_edges if b == m}:
            S.add(m)


for n in L:
    if n.startswith("output"):
        continue
    low,high = sorted(values[n])
    lo,ho = sorted([(b,c) for a,b,c in edges if a == n], key=lambda p: p[1])
    values[lo[0]].append(low)
    values[ho[0]].append(high)

part1 = int([k for k,v in values.items() if sorted(v) == [17,61]][0].split(" ")[1])
print("Part 1:", part1)

part2 = 0
print("Part 2:", values["output 0"][0]*values["output 1"][0]*values["output 2"][0])
