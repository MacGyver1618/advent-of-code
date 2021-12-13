from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = to_nums(lines(7)[0].split(","))

part1 = min([sum([abs(x-y) for x in inpt]) for y in range(min(inpt), max(inpt)+1)])
print("Part 1:", part1)

part2 = min([sum([abs(x-y)*(abs(x-y)+1)//2 for x in inpt]) for y in range(min(inpt), max(inpt)+1)])
print("Part 2:", part2)
