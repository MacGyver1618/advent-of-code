from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(21)

res = [
    r"swap position (.) with position (.)",
    r"swap letter (.) with letter (.)",
    r"rotate (left|right) (.) steps?",
    r"rotate based on position of letter (.)",
    r"reverse positions (.) through (.)",
    r"move position (.) to position (.)"
]

s = "abcdefgh"

def swap(s, x, y):
    s = [*s]
    t = s[x]
    s[x] = s[y]
    s[y] = t
    return "".join(s)

def swapl(s, x, y):
    return swap(s, s.index(x), s.index(y))

def rot(s, dir, steps):
    s = coll.deque(s)
    steps = -int(steps) if dir == "left" else int(steps)
    s.rotate(steps)
    return "".join(s)

def rotl(s, l):
    s = coll.deque(s)
    i = s.index(l)
    steps = i + (1 if i < 4 else 2)
    s.rotate(steps)
    return "".join(s)

def rev(s, x, y):
    head = s[0:x]
    subs = s[x:y+1]
    tail = s[y+1:]
    return "".join([head, "".join([*reversed(subs)]), tail])

def mov(s, x, y):
    #TODO
    s = coll.deque(s)
    s.rotate(-x)
    t = s.popleft()
    s.rotate(x-y)
    s.appendleft(t)
    s.rotate(y)
    return "".join(s)

for line in inpt:
    if re.match(res[0], line):
        s = swap(s, *map(int, re.match(res[0], line).groups()))
    if re.match(res[1], line):
        s = swapl(s, *re.match(res[1], line).groups())
    if re.match(res[2], line):
        s = rot(s, *re.match(res[2], line).groups())
    if re.match(res[3], line):
        s = rotl(s, *re.match(res[3], line).groups())
    if re.match(res[4], line):
        s = rev(s, *map(int, re.match(res[4], line).groups()))
    if re.match(res[5], line):
        s = mov(s, *map(int, re.match(res[5], line).groups()))

print("Part 1:", s)

s = "fbgdceah"
for line in reversed(inpt):
    if re.match(res[0], line):
        s = swap(s, *map(int, re.match(res[0], line).groups()))
    if re.match(res[1], line):
        s = swapl(s, *re.match(res[1], line).groups())
    if re.match(res[2], line):
        dir, amt = re.match(res[2], line).groups()
        dir = "left" if dir == "right" else "right"
        s = rot(s, dir, amt)
    if re.match(res[3], line):
        l, = re.match(res[3], line).groups()
        i = s.index(l)
        if i == 0:
            amt = 1
        elif i == 1:
            amt = 1
        elif i == 2:
            amt = 6
        elif i == 3:
            amt = 2
        elif i == 4:
            amt = 7
        elif i == 5:
            amt = 3
        elif i == 6:
            amt = 0
        elif i == 7:
            amt = 4
        s = rot(s, "left", str(amt))
    if re.match(res[4], line):
        s = rev(s, *map(int, re.match(res[4], line).groups()))
    if re.match(res[5], line):
        s = mov(s, *map(int, reversed(re.match(res[5], line).groups())))

print("Part 2:", s)
