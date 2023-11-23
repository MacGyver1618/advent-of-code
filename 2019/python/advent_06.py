import copy

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

nodes=set()
edges=set()
for line in lines:
    a,b=line.split(")")
    nodes.add(a)
    nodes.add(b)
    edges.add((b,a))

orbits=0
for node in nodes:
    path_to_com=bfs(node,eq("COM"),lambda n: [b for a,b in edges if a==n])
    orbits+=len(path_to_com)-1

part1 = orbits
print("Part 1:", part1)
start=[b for a,b in edges if a=="YOU"][0]
end=[b for a,b in edges if a=="SAN"][0]
new_edges=copy.deepcopy(edges)
for a,b in edges:
    new_edges.add((b,a))
part2 = len(bfs(start,eq(end),lambda n: [b for a,b in new_edges if a==n]))-1
print("Part 2:", part2)
