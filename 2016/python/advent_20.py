from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(20)

def to_range(s):
    return tuple(map(int, re.match(r"(\d+)-(\d+)", s).groups()))

ranges = sorted(map(to_range, inpt))

def collapse_ranges():
    cur = ranges[0]
    for range in ranges[1:]:
        if range[0] <= cur[1] + 1:
            cur = (min(cur[0], range[0]), max(cur[1], range[1]))
        else:
            yield cur
            cur = range
    yield cur

collapsed = [*collapse_ranges()]

part1 = collapsed[0][1]+1

print("Part 1:", part1)

gaps = zip(map(lambda x: x[0], collapsed[1:]), map(lambda x: x[1], collapsed[:-1]))
diffs = map(lambda pair: oper.sub(*pair)-1, gaps)
part2 = sum(diffs) + 2**32-1-collapsed[-1][1]
print("Part 2:", part2)
