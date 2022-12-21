import timeit

from common.advent_lib import *
from collections import Counter, defaultdict, deque
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

def exec():
    elves = full_input(1).split("\n\n")
    cals = [sum(to_nums(elf.split())) for elf in elves]

    print("Part 1:", max(cals))
    print("Part 2:", sum(sorted(cals)[-3:]))


print(timeit.timeit(exec, number=1))
