from common.advent_lib import *
import hashlib
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

passcode = read_lines(17)[0]

OPEN = "bcdef"

tgt = A([3,3])

def locks(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:4]

def neighbors(path):
    p = sum(map(directions.get, path)) if path else O
    if (p == tgt).all():
        return []
    u, d, l, r = locks(passcode + path)
    if u in OPEN and p[1] > 0:
        yield path + "U"
    if d in OPEN and p[1] < 3:
        yield path + "D"
    if l in OPEN and p[0] > 0:
        yield path + "L"
    if r in OPEN and p[0] < 3:
        yield path + "R"

Q = coll.deque()
Q.append("")
seen = set()

while Q:
    cur = Q.popleft()
    seen.add(cur)
    for n in neighbors(cur):
        Q.append(n)


def is_end(path):
    pos = sum(map(directions.get, path)) if cur else O
    return (pos == tgt).all()


paths_to_end = [*filter(is_end, seen)]

print("Part 1:", min(paths_to_end, key= len))
print("Part 2:", max(map(len, paths_to_end)))
