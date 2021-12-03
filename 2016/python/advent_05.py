from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
from hashlib import md5

inpt = lines(5)[0]

i = 0
pw = ""
part2 = list("________")
while len(pw) < 8 or part2.count("_") != 0:
    seed = inpt + str(i)
    cs = md5(seed.encode("utf-8")).hexdigest()
    if cs.startswith("00000"):
        if cs[5] in "12345670":
            pos = int(cs[5])
            char = cs[6]
            if part2[pos] == '_':
                part2[pos] = char
                print("".join(part2))
        if len(pw) < 8:
            pw += cs[5]
            print(pw)
    i += 1

print("Part 1:", pw)

print("Part 2:", "".join(part2))
