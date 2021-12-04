from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

I = lines(4)

tot = 0
reals = []
for l in I:
    n,_,i,c = re.match(r"([a-z]+(-[a-z]+)+)-(\d+)\[([a-z]+)\]", l).groups()
    orig = n
    n = n.replace("-","")
    C = coll.Counter(n)
    by_char = sorted(C.items())
    cs = "".join(it2.take(5, map(it2.first, sorted(by_char, key=lambda i: i[1], reverse=True))))
    if cs == c:
        tot += int(i)
        reals.append((orig, int(i)))

print("Part 1:", tot)

abc = "abcdefghijklmnopqrstuvwxyz"

rooms = {}
for real,rot in reals:
    shifted = coll.deque(abc)
    shifted.rotate(rot)
    cipher = dict([*zip(shifted,abc)])
    s = ""
    for c in real:
        s += " " if c == "-" else cipher[c]
    rooms[s] = rot

print("Part 2:", rooms["northpole object storage"])
