from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

card = 14012298
door = 74241

c = 1
for i in it.count(1):
    c = c*7 % 20201227
    if c == card:
        cloop = i
        break

part1 = pow(door, cloop, 20201227) % 20201227

print("Part 1:", part1)

print("Part 2: DONE")
