from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = to_nums(lines(20))[0]

part1 = 0

for n in it.count(1):
    if 10*sum(sym.divisors(n)) >= inpt:
        break

print("Part 1:", n)

for n in it.count(1):
    if 11*sum(filter(lambda x: n // x <= 50, sym.divisors(n))) >= inpt:
        break

print("Part 2:", n)
