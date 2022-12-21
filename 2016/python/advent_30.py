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

inpt = read_lines(1)
ds = inpt[0].split(", ")

d = 1j
pos = 0
visited = set()
part2 = None

for direction in ds:
    if direction[0] == 'L':
        d *= 1j
    elif direction[0] == 'R':
        d *= -1j
    amt = int(direction[1:])
    while amt > 0:
        pos += 1*d
        if pos in visited and part2 is None:
            part2 = pos
        amt -= 1
        visited.add(pos)

part1 = 0
print("Part 1:", int(abs(pos.real) + abs(pos.imag)))

print("Part 2:", int(abs(part2.real) + abs(part2.imag)))
