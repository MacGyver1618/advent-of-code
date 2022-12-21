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

lines = read_lines(10)

X = 1
tot = 0
time = 0
wait = False
add = False
incoming = 0
pc = 0
s = ""

while pc < len(lines):
    cycle = time+1
    if cycle % 40 == 20:
        tot += cycle*X
    if wait:
        wait = False
        add = True
    else:
        line = lines[pc]
        if line.startswith("addx"):
            incoming = int(line.split()[1])
            wait = True
        else:
            pc += 1
    s += "#" if X-1 <= time%40 <= X+1 else " "
    if add:
        X += incoming
        add = False
        pc += 1
    time += 1
print("\n".join([s[i:i+40] for i in range(0, len(s), 40)]))

print("Part 1:", tot)
print("Part 2:", "See above")

vals = [1]
for line in read_lines(10):
    cur = vals[-1]
    vals += [cur] if line == "noop" else [cur, cur+int(line.split()[1])]
print(sum(i*vals[i-1] for i in range(20,len(vals), 40)))
s = "".join("#" if v-1 <= i % 40 <=v+1 else " " for i,v in enumerate(vals))
print("\n".join([s[i:i+40] for i in range(0, len(s), 40)]))