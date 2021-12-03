from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

init = lines(16)[0]

def expand(s):
    return s + "0" + "".join(["1" if x == "0" else "0" for x in reversed(s)])

disk = init
while len(disk) < 272:
    disk = expand(disk)

def checksum(s):
    chunks = [s[i:i+2] for i in range(0, len(s), 2)]
    cs = "".join(["1" if chunk[0] == chunk[1] else "0" for chunk in chunks])
    if len(cs) % 2 != 0:
        return cs
    return checksum(cs)


print("Part 1:", checksum(disk[:272]))

disk = init
while len(disk) < 35651584:
    disk = expand(disk)
print("Part 2:", checksum(disk[:35651584]))
