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
sensors = set()
beacons = set()

distances = defaultdict(int)

for line in lines:
    sx,sy,bx,by = to_nums(re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line).groups())
    sensor = (sx, sy)
    beacon = (bx, by)
    sensors.add(sensor)
    beacons.add(beacon)
    dist = manhattan_distance(sensor, beacon)
    distances[sensor] = dist

distances = sorted(distances.items(), key=lambda x: first(first(x)))

def join_spills(a, b):
    if a[0] > b[1]+1:
        return [b,a]
    elif a[1] < b[0]-1:
        return [a,b]
    else:
        return [[min(a[0], b[0]), max(a[1], b[1])]]

def combine_all(spills):
    if len(spills) < 2:
        return spills
    result = []
    cur, *rest = spills
    for spill in rest:
        joined = join_spills(cur, spill)
        if len(joined) > 1:
            result.append(joined[0])
            cur = joined[1]
    result.append(cur)
    return result

def insert_spill(spills, spill):
    if not spills:
        return [spill]
    new_spills = []
    for spill2 in spills:
        new_spills += join_spills(spill, spill2)
    return combine_all(new_spills)

def spills_at(row):
    spills = []
    for i,[(x,y),d] in enumerate(distances):
        dr = d - abs(row-y)
        if dr >= 0:
            spills = insert_spill(spills, [x - dr, x + dr])
    return spills
Y = 2
false_bs = [p for p in beacons if p[1] == Y]
part1 = sum(s[1]-s[0]+1 for s in spills_at(Y))-len(false_bs)
print("Part 1:", part1)

for i in range(4_000_001):
    spills = spills_at(i)
    if len(spills) > 1:
        part2 = 4_000_000*(spills[0][1]+1)+i
        break

print("Part 2:", part2)
