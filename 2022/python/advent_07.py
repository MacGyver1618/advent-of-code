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

fs = defaultdict(int)

path = tuple()
for line in lines:
    if line.startswith("$"):
        _, *rest = line.split()
        if rest[0] == "ls":
            continue
        else: # cmd = cd
            _, dirname = rest
            if dirname == "..":
                path = tuple(path[:-1])
            elif dirname == "/":
                path = tuple()
            else:
                path += dirname,
    else: # directory listing
        sym, name = line.split()
        if sym == "dir":
            continue
        else:
            fs[path] += int(sym)

recursive_sizes = defaultdict(int)

for entry in fs.items():
    k, v = entry
    cur = tuple()
    for dirname in k:
        cur += dirname,
        recursive_sizes[cur] += v

part1 = sum(v for v in recursive_sizes.values() if v <= 100000)
print("Part 1:", part1)

used = sum(fs.values())
avail = int(7e7) - used
needed = int(3e7) - avail

part2 = min(v for v in recursive_sizes.values() if v >= needed)
print("Part 2:", part2)
