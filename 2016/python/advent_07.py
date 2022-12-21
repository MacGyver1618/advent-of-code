from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(7)

abbas = [a+b+b+a for a in abc for b in abc if a != b]
def has_abba(s):
    return sum([s.count(abba) for abba in abbas]) != 0

part1 = 0
part2 = 0
for line in inpt:
    toks = re.split(r"[\[\]]", line)
    hnets = toks[1::2]
    snets = toks[::2]
    if any([has_abba(s) for s in snets]) and not any([has_abba(s) for s in hnets]):
        part1 += 1
    if any([hnet.count(a+b+a) != 0 and snet.count(b+a+b) != 0 for hnet in hnets for snet in snets for a in abc for b in abc if a != b]):
        part2 += 1

print("Part 1:", part1)


print("Part 2:", part2)
