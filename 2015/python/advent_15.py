from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
from numpy import array as A

inpt = lines(15)
ingredients = []
for line in inpt:
    name, rest = line.split(": ")
    props = rest.split(", ")
    d = tuple()
    for prop in props:
        _,v = prop.split(" ")
        d += int(v),
    ingredients.append(d)

combinations = []

for i in range(101):
    for j in range(101):
        for k in range(101):
            for l in range(101):
                if i+j+k+l != 100:
                    continue
                else:
                    combinations.append((i,j,k,l))

max_score = 0
best_cookie = 0
for sp, pb, fr, su in combinations:
    sps = sp * A(ingredients[0])
    pbs = pb * A(ingredients[1])
    frs = fr * A(ingredients[2])
    sus = su * A(ingredients[3])
    scores = (sps,pbs,frs,sus)
    cap = max(0, sum([s[0] for s in scores]))
    dur = max(0, sum([s[1] for s in scores]))
    fla = max(0, sum([s[2] for s in scores]))
    tex = max(0, sum([s[3] for s in scores]))
    cal = max(0, sum([s[4] for s in scores]))
    score = np.prod([cap,dur,fla,tex])
    max_score = max(score, max_score)
    if cal == 500:
        best_cookie = max(score, best_cookie)

print("Part 1:", max_score)

print("Part 2:", best_cookie)
