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
import json

pairs = full_input(13).strip().split("\n\n")

part1 = 0

def compare(a, b):
    for n in range(max(len(a), len(b))):
        if n == len(a):
            return -1
        left = a[n]
        if n == len(b):
            return 1
        right = b[n]
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return -1
            if left > right:
                return 1
        if isinstance(left, list) and isinstance(right, list):
            cmp = compare(left, right)
            if cmp == 0:
                continue
            return cmp
        if isinstance(left, list) and isinstance(right, int):
            cmp = compare(left, [right])
            if cmp == 0:
                continue
            return cmp
        if isinstance(left, int) and isinstance(right, list):
            cmp = compare([left], right)
            if cmp == 0:
                continue
            return cmp
    return 0

for i, pair in enumerate(pairs):
    a, b = map(json.loads, pair.split("\n"))
    if compare(a, b) == -1:
        part1 += i+1

print("Part 1:", part1)

div1, div2 = [[2]], [[6]]
packets = [div1,div2]
for pair in pairs:
    packets += [*map(json.loads, pair.split("\n"))]

packets = sorted(packets, key=func.cmp_to_key(compare))
print("\n".join(map(str, packets)))
part2 = inc(packets.index(div1))*inc(packets.index(div2))
print("Part 2:", part2)
