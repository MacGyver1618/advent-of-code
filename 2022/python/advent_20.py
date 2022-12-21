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
nums = [(int(v),i) for i,v in enumerate(read_lines(20))]
buffer = deque(nums)
l = len(nums)
for n in nums:
    buffer.rotate(-buffer.index(n))
    num,_ = buffer.popleft()
    buffer.rotate(-num)
    buffer.appendleft(n)

z = [(v,i) for v,i in nums if v == 0][0]
buffer.rotate(-buffer.index(z))
part1 = sum(buffer[n][0] for n in [1000,2000,3000])
print("Part 1:", part1)

nums = [(v*811589153,i) for v,i in nums]
buffer = deque(nums)

for _ in range(10):
    for n in nums:
        buffer.rotate(-buffer.index(n))
        num = buffer.popleft()
        buffer.rotate(-num[0])
        buffer.appendleft(num)

buffer.rotate(-buffer.index(z))
part2 = sum(buffer[n][0] for n in [1000,2000,3000])
print("Part 2:", part2)
