from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(17)

xmin, xmax, ymin, ymax = map(int, re.match(r"target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)", inpt[0]).groups())

mins = A([xmin, ymin])
maxs = A([xmax, ymax])

def increment(v):
    vx,vy = v
    return A([max(dec(vx), 0), dec(vy)])

peaks = {}

for vx in range(1,200):
    for vy in range(-200,200):
        p = O.copy()
        v = A([vx,vy])
        orig = tuple(v)
        highest = -float("inf")
        while True:
            highest = max(p[1], highest)
            if (p >= mins).all() and (p <= maxs).all():
                peaks[orig] = highest
                break
            if p[0] > xmax or p[1] < ymin:
                break
            p += v
            v = increment(v)

print("Part 1:", max(peaks.values()))
print("Part 2:", len(peaks))
