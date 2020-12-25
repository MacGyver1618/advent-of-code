from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(19)
SPLIT = 131
# SPLIT = 31

edges = []
rules = {}
literals = {}

S = set()
L = []

for line in inpt[:SPLIT]:
    n, rs = line.split(": ")
    rules[int(n)] = rs
    literals[int(n)] = rs
    for r in rs.split(" | "):
        for e in r.split(" "):
            if not re.match(r"\"[ab]\"", e):
                edges.append((int(e), int(n)))
            else:
                literals[int(n)] = e.replace("\"","")
                S.add(int(n))

E2 = edges.copy()

while S:
    n = S.pop()
    L.append(n)
    for e in [(a,b) for a,b in E2 if a == n]:
        _,m = e
        E2.remove(e)
        if not [1 for a,b in E2 if b == m and a != n]:
            S.add(m)

print(L)

for n in L:
    print(n, ":", rules[n], "=", literals[n])
    l = literals[n]
    for m in [b for a,b in edges if a == n]:
        r = literals[m]
        literals[m] = re.sub(re.compile("(?<!\d)%s(?!\d)" % str(n)), "("+l+")", r)

for k,v in literals.items():
    literals[k] = v.replace(" ", "")

regex = "(" + literals[0] + ")"
print(regex)
part1 = 0
for line in inpt[SPLIT+1:]:
    if re.fullmatch(re.compile(regex), line):
        part1 += 1
print("Part 1:", part1)

print("42:", literals[42])
print("31:", literals[31])

rules[8] = "42 | 42 8"
rules[11] = "42 31 | 42 11 31"

x = "(" + literals[42] + ")"
y = "(" + literals[31] + ")"

regex2 = "x+(xy|xxyy|xxxyyy)".replace("x", x).replace("y", y)

xr = re.compile(x)
yr = re.compile(y)


print(regex2)
part2 = 0

for line in inpt[SPLIT+1:]:
    if re.fullmatch(re.compile(regex2), line):
        part2 += 1
print("Part 2:", part2)
