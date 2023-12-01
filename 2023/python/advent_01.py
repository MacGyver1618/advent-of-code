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

lines = read_lines(1)

tot=0
for line in lines:
    ints=[*map(int,re.findall(r"\d",line))]
    tot+=int(str(ints[0])+str(ints[-1]))

part1 = tot
print("Part 1:", part1)

nums=["zero","one","two","three","four","five","six","seven","eight","nine"]
tot=0
for line in lines:
    poss=[-1]*len(line)
    for i,c in enumerate(line):
        if c.isnumeric():
            poss[i]=int(c)
        for num in nums:
            if line[i:].startswith(num):
                poss[i]=nums.index(num)
    ints=[pos for pos in poss if pos != -1]
    tot+=int(str(ints[0])+str(ints[-1]))
part2=tot
print("Part 2:", part2)
