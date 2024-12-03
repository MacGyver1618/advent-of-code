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

lines = read_lines(2)

part1=0
part2=0

def is_safe(nums):
    diff=[a-b for a,b in zip(nums[1:],nums[:-1])]
    monot=all(d < 0 for d in diff) or all(d > 0 for d in diff)
    d2=all(abs(d) <= 3 for d in diff)
    return monot and d2

for line in lines:
    nums=parse_ints(line)
    if is_safe(nums):
        part1+=1
        part2+=1
        continue
    for i in range(len(nums)):
        n2=[n for j,n in enumerate(nums) if i!=j]
        if is_safe(n2):
            part2+=1
            break

print("Part 1:", part1)
print("Part 2:", part2)
