from advent_lib import *
import re
import functools as func
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym
import json
import collections as coll

inpt = lines(12)[0]

nums = re.split(r"[^-0-9]+", inpt)[1:-1]

print("Part 1:", sum(map(int, nums)))

tree = json.loads(inpt)
Q = coll.deque()
tot = 0
Q.append(tree)
while Q:
    n = Q.pop()
    t = type(n)
    if t == dict:
        if "red" in n.values():
            continue
        Q.extend(n.values())
    elif t == list:
        Q.extend(n)
    elif t == str:
        continue
    elif t == int:
        tot += n

print("Part 2:", tot)
