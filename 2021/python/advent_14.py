from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(14)

seed = inpt[0]

rules = {}

for line in inpt[2:]:
    pair, between = line.split(" -> ")
    rules[pair] = between

molecule = seed

for _ in range(10):
    prev = molecule[0]
    next_m = prev
    for c in molecule[1:]:
        ss = prev + c
        if ss in rules:
            next_m += rules[ss]
        next_m += c
        prev = c
    molecule = next_m

counts = coll.Counter(molecule).values()
print("Part 1:", max(counts) - min(counts))

C = coll.Counter()
for SS in [seed[i-1:i+1] for i in range(1, len(seed))]:
    C[SS] += 1

for _ in range(40):
    next_C = coll.Counter()
    for pair in C:
        next_C[pair[0]+rules[pair]] += C[pair]
        next_C[rules[pair]+pair[1]] += C[pair]
    C = next_C

elems = coll.Counter()
for k,v in C.items():
    elems[k[0]] += v
elems[seed[-1]] += 1

print("Part 2:", max(elems.values())-min(elems.values()))
