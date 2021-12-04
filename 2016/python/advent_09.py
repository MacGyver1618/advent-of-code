from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(9)[0]
file = inpt

ver1 = 0
while file:
    match = re.search(r"\([0-9x]+\)", file)
    if not match:
        ver1 += len(file)
        break
    chars,times = to_nums(match.group(0)[1:-1].split("x"))
    start = match.start()
    end = match.end()
    ver1 += start
    ver1 += chars*times
    file = file[end+chars:]

print("Part 1:", ver1)

ver2 = 0

def expand(s):
    match = re.search(r"\([0-9x]+\)", s)
    if not match:
        return len(s)
    chars,times = to_nums(match.group(0)[1:-1].split("x"))
    start = match.start()
    end = match.end()
    before = s[:start]
    group = s[end:end+chars]
    after = s[end+chars:]
    return expand(before) + times*expand(group) + expand(after)

print("Part 2:", expand(inpt))
