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

lines = read_lines(11)
stones=Counter([int(i) for i in lines[0].split()])

for i in range(75):
    if i == 25:
        part1=sum(stones.values())
    nxt=Counter()
    for stone, count in stones.items():
        if stone==0:
            nxt[1]+=count
        elif len(str(stone))%2==0:
            s=str(stone)
            l=len(s)
            a=int(s[:l//2])
            b=int(s[l//2:])
            nxt[a]+=count
            nxt[b]+=count
        else:
            nxt[2024*stone]+=count
    stones=nxt

print("Part 1:", part1)
part2 = sum(stones.values())
print("Part 2:", part2)
