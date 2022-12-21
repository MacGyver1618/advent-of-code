from time import time

from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

cups = coll.deque(to_nums(read_lines(23)[0][:]))

for _ in range(100):
    current = cups.popleft()
    pickup = [cups.popleft(), cups.popleft(), cups.popleft()]
    destination = current - 1
    while destination in pickup or destination < 1:
        destination -= 1
        if destination < 1:
            destination = 9
    cups.appendleft(current)
    rotation = 0
    while cups[0] != destination:
        cups.rotate(-1)
        rotation += 1
    cups.rotate(-1)
    cups.extendleft(reversed(pickup))
    cups.rotate(rotation)

cups.rotate(-cups.index(1))
cups.popleft()

print("Part 1:", "".join(map(str, cups)))

cups = coll.deque(to_nums(read_lines(23)[0][:]))
cups.extend(range(10,1_000_001))
nexts = cups.copy()
nexts.rotate(-1)

followers = {}

for cup,nxt in zip(cups, nexts):
    followers[cup] = nxt

current = cups[-1]
for _ in range(10_000_000):
    current = followers[current]
    pickup = [followers[current], followers[followers[current]], followers[followers[followers[current]]]]
    destination = current - 1
    while destination in pickup or destination < 1:
        destination -= 1
        if destination < 1:
            destination = 1_000_000
    followers[current] = followers[pickup[-1]]
    tmp = followers[destination]
    followers[destination] = pickup[0]
    followers[pickup[2]] = tmp

c = followers[1]
part2 = c*followers[c]

print("Part 2:", part2)
