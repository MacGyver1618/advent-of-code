from advent_lib import *
import re
import functools as func
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(14)
regex = r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\."

reindeer = {}
for line in inpt:
    r,s,w,p = re.match(regex, line).groups()
    reindeer[r] = (int(s),int(w),int(p),int(w)+int(p))

def dist_at(r, t):
    speed,work,rest,total = reindeer[r]
    cycles = t // total
    rem = t % total
    dist = speed*(work*cycles + min(rem, work))
    return dist

print("Part 1:", max(map(lambda r: dist_at(r, 2503), reindeer.keys())))

points = {}
dists = {}
for r in reindeer.keys():
    dists[r] = 0
    points[r] = 0

for t in range(2503):
    for r in reindeer:
        speed,work,rest,total = reindeer[r]
        if (t // total)*total + work > t:
            dists[r] += speed
    leader = it2.first(sorted(dists.items(), key=lambda item: item[1], reverse=True))[0]
    points[leader] += 1

print("Part 2:", max(points.values()))
