from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(6)

poss = coll.defaultdict(coll.Counter)

for line in inpt:
    for i,c in enumerate(line):
        poss[i].update([c])
part1 = ""
part2 = ""
for i in range(8):
    part1 += poss[i].most_common(1)[0][0]
    part2 += poss[i].most_common()[-1][0]

print("Part 1:", part1)

print("Part 2:", part2)
