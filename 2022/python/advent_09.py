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

lines = read_lines(9)

def move(num_knots):
    s = O
    h = s.copy()
    knots = [s.copy() for _ in range(num_knots)]
    visited = set(tuple(s))

    for line in lines:
        dir, amt = line.split()
        for _ in range(int(amt)):
            h += directions[dir]
            prev = h
            new_knots = []
            for i, t in enumerate(knots):
                d = prev - t
                if max(abs(d)) > 1:
                    t += np.sign(d)
                    if i == num_knots - 1:
                        visited.add(tuple(t))
                new_knots.append(t)
                prev = t
            knots = new_knots
    return len(visited)

print("Part 1:", move(1))
print("Part 2:", move(9))
