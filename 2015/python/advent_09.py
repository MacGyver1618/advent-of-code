from advent_lib import *
import re
import functools as func
import itertools as it
import numpy as np
import sympy as sym

inpt = lines(9)

vertices = set()
dists = {}
for line in inpt:
    a,b,dist = re.match(r"(\w+) to (\w+) = (\d+)", line).groups()
    vertices.add(a)
    vertices.add(b)
    dists[(a,b)] = int(dist)
    dists[(b,a)] = int(dist)

def lengths():
    for path in it.permutations(vertices):
        segments = [*zip(path, path[1:])]
        yield sum(map(dists.get, segments))

print("Part 1:", min(lengths()))

print("Part 2:", max(lengths()))
