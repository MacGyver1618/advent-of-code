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

lines = read_lines(15)
A_value=int(lines[0].split()[-1])
B_value=int(lines[1].split()[-1])
A_factor=16807
B_factor=48271
divisor=2147483647
bitmask=0b1111111111111111

total=0
for _ in range(40_000_000):
    A_value=(A_value*A_factor)%divisor
    B_value=(B_value*B_factor)%divisor
    if A_value&bitmask==B_value&bitmask:
        total+=1

part1 = total
print("Part 1:", part1)

A_value=int(lines[0].split()[-1])
B_value=int(lines[1].split()[-1])

def generate(value, factor, multiple_of):
    next_val=(value*factor)%divisor
    return next_val if next_val%multiple_of == 0 else generate(next_val, factor, multiple_of)


part2 = 0
for _ in range(5_000_000):
    A_value=generate(A_value, A_factor, 4)
    B_value=generate(B_value, B_factor, 8)
    if A_value&bitmask==B_value&bitmask:
        part2+=1


print("Part 2:", part2)
