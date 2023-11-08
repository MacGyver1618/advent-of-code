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
nums = to_nums(read_lines(20))

def solve(numbers, rounds):
    l = len(numbers)
    enumerated = [*enumerate(numbers)]
    Q = deque(enumerated)
    for _ in range(rounds):
        for n in enumerated:
            Q.rotate(-Q.index(n))
            _,num = Q.popleft()
            Q.rotate(-num)
            Q.appendleft(n)
    vals = [num for _,num in Q]
    z = vals.index(0)
    return sum(vals[(z+n)%l] for n in [1000,2000,3000])

print("Part 1:", solve(nums, 1))

print("Part 2:", solve([n*811589153 for n in nums], 10))
