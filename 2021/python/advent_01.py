from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = to_nums(lines(1))

part1 = sum([1 for i in range(1,len(inpt)) if inpt[i] > inpt[i-1]])

print("Part 1:", part1)

part2 = sum([1 for i in range(3,len(inpt)) if inpt[i] > inpt[i-3]])

print("Part 2:", part2)
