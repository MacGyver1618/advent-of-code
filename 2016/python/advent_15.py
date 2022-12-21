from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(15)
discs = set()

for line in inpt:
    ds = re.match(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).", line).groups()
    discs.add(tuple(map(int, ds)))

def passes(n):
    for disc in discs:
        disc, mod, rem = disc
        if (rem + n + disc) % mod != 0:
            return False
    return True

i = 0
while True:
    if passes(i):
        part1 = i
        break
    i += 1

print("Part 1:", part1)

discs.add((len(discs)+1,11,0))

i = 0
while True:
    if passes(i):
        part2 = i
        break
    i += 1
print("Part 2:", part2)
