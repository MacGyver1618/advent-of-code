from advent_lib import *
import re
import functools as func
import itertools as it
import operator as oper
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(10)[0]

def rle(s):
    gs = re.split(r"(?<=(.))(?!\1)", s)[:-1:2]
    out = ""
    for g in gs:
        out += str(len(g))
        out += g[0]
    return out

part1 = it2.nth(it2.iterate(rle, inpt), 40)
print("Part 1:", len(part1))

part2 = it2.nth(it2.iterate(rle, part1), 10)
print("Part 2:", len(part2))
