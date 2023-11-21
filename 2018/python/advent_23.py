import heapq

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
from queue import PriorityQueue
lines = read_lines(23)

bots=[]
for line in lines:
    x,y,z,r=map(int,re.findall(r"-?\d+",line))
    bots += [(x,y,z,r)]

max_r=max(bots, key=lambda b:b[3])
part1 = sum(1 for bot in bots if manhattan_distance(bot[:3],max_r[:3])<=max_r[3])
print("Part 1:", part1)

@func.cache
def bots_in_range(c):
    return sum(1 for bot in bots if manhattan_distance(bot[:3], c) <= bot[3])

r=2**28
box=((-r,-r,-r),(r,r,r))


# Part 2 copied from Reddit, still don't exactly know how this method actually works
def does_intersect(box, bot):
    # returns whether box intersects bot
    d = 0
    for i in (0, 1, 2):
        boxlow, boxhigh = box[0][i], box[1][i] - 1
        d += abs(bot[i] - boxlow) + abs(bot[i] - boxhigh)
        d -= boxhigh - boxlow
    d //= 2
    return d <= bot[3]


def intersect_count(box):
    return sum(1 for b in bots if does_intersect(box, b))

workheap = [(-len(bots), -2*r, 3*r, box)]
while workheap:
    (negreach, negsz, dist_to_orig, box) = heapq.heappop(workheap)
    if negsz == -1:
        part2=manhattan_distance(box[0],(0,0,0))
        break
    newsz = negsz // -2
    for octant in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                   (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
        newbox0 = tuple(box[0][i] + newsz * octant[i] for i in (0, 1, 2))
        newbox1 = tuple(newbox0[i] + newsz for i in (0, 1, 2))
        newbox = (newbox0, newbox1)
        newreach = intersect_count(newbox)
        heapq.heappush(workheap,
                       (-newreach, -newsz, manhattan_distance(newbox0, (0, 0, 0)), newbox))

print("Part 2:", part2)
