from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = to_nums(lines(17))

sets = [comb for comb in powerset(inpt) if sum(comb) == 150]
part1 = len(sets)
print("Part 1:", part1)

part2 = len([comb for comb in sets if len(comb) == min(map(len, sets))])
print("Part 2:", part2)
