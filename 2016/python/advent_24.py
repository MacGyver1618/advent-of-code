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

lines = read_lines(24)
grid=dict()
targets=dict()

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char in "0123456789":
            targets[char]=(r,c)
            grid[(r,c)]="."
        else:
            grid[(r,c)]=char

def neighbor_fn(p):
    for n in adjacent(p):
        n = tuple(n)
        if n in grid and grid[n]!="#":
            yield n

paths=dict()
for start in targets:
    for end in targets:
        if start != end:
            paths[f"{start}{end}"] = bfs(targets[start], eq(targets[end]),neighbor_fn)

minlen=float("inf")
for perm in it.permutations("1234567"):
    path="0"+"".join(perm)
    plen=0
    for i in range(len(path)-1):
        plen+=len(paths[path[i:i+2]])-1
    if plen < minlen:
        minlen=plen

part1 = minlen
print("Part 1:", part1)

minlen=float("inf")
for perm in it.permutations("1234567"):
    path="0"+"".join(perm)+"0"
    plen=0
    for i in range(len(path)-1):
        plen+=len(paths[path[i:i+2]])-1
    if plen < minlen:
        minlen=plen

part2 = minlen
print("Part 2:", part2)
