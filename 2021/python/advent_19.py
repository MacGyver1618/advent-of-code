from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(19)

scanners = coll.defaultdict(list)

rotations = [
    # Rotation about the X axis
    A([[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]]),
    A([[ 1, 0, 0],[ 0, 0,-1],[ 0, 1, 0]]),
    A([[ 1, 0, 0],[ 0,-1, 0],[ 0, 0,-1]]),
    A([[ 1, 0, 0],[ 0, 0, 1],[ 0,-1, 0]]),
    # Rotation about the Y axis
    A([[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]]),
    A([[ 0, 0,-1],[ 0, 1, 0],[ 1, 0, 0]]),
    A([[-1, 0, 0],[ 0, 1, 0],[ 0, 0,-1]]),
    A([[ 0, 0, 1],[ 0, 1, 0],[-1, 0, 0]]),
    # Rotation about the Z axis
    A([[ 1, 0, 0],[ 0, 1, 0],[ 0, 0, 1]]),
    A([[ 0,-1, 0],[ 1, 0, 0],[ 0, 0, 1]]),
    A([[-1, 0, 0],[ 0,-1, 0],[ 0, 0, 1]]),
    A([[ 0, 1, 0],[-1, 0, 0],[ 0, 0, 1]]),
]

rs = [*map(A, set([tuple(map(tuple, r1@r2)) for r1 in rotations for r2 in rotations]))]

for line in inpt:
    if not line:
        continue
    if line.startswith("---"):
        scanner = int(line.split()[2])
        continue
    p = tuple(map(int, line.split(",")))
    scanners[scanner].append(p)

beacons = set(scanners[0])
Q = coll.deque(bs for bs in [*scanners.items()][1:])
positions = {(0,0,0)}

while Q:
    cur, bs = Q.popleft()
    hit = False
    for r in rs:
        if hit:
            break
        rotated = [r@b for b in bs]
        dists = coll.Counter(tuple(b2-b1) for b2 in rotated for b1 in beacons)
        [(offset,count)] = dists.most_common(1)
        if count >= 12:
            print("hit with", cur, "at", offset)
            hit = True
            beacons |= set(tuple(b-offset) for b in rotated)
            positions.add(offset)
    if not hit:
        Q.append((cur,bs))


print("Part 1:", len(beacons))

part2 = max(manhattan_distance(a,b) for a in positions for b in positions)
print("Part 2:", part2)
