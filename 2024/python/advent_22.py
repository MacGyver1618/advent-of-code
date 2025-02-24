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

lines = read_lines(22)
grid=Grid(lines)
R = len(lines)
C = len(lines[0])

def gen(seed):
    def _gen():
        n=seed
        while True:
            n=(n*64)^seed
            n%=16777216
            n//=32
            n^=seed
            n%=16777216
            n*=2048
            n^=seed
            n%=16777216
            yield seed
    return _gen

def mix():
    ...

prices=[[] for _ in range(len(lines))]
diffs=[[] for _ in range(len(lines))]
part1 = 0
for i,line in enumerate(lines):
    seed=int(line)
    n=seed
    prev=n%10
    for _ in range(2000):
        n=((n<<6)^n)&(2**24-1)
        n=((n>>5)^n)&(2**24-1)
        n=((n<<11)^n)&(2**24-1)
        prices[i]+=[n%10]
        diffs[i]+=[(n % 10) - prev]
        prev=n%10
    part1+=n

print("Part 1:", part1)

strs=[''.join(chr(75+k) for k in diff) for diff in diffs]

part2 = 0
pb=ProgressBar(19**4)
for i in range(19**4):
    pb.update()
    ks=[i%19-9, (i//19)%19-9, (i//(19**2))%19-9, (i//(19**3))%19-9]
    seq="".join(chr(75+k) for k in ks)
    bananas=0
    for j,s in enumerate(strs):
        try:
            idx=s.index(seq)
            bananas+=prices[j][idx+3]
        except Exception:
            pass
        # input()
    if bananas>part2:
        part2=bananas

pb.clear()


print("Part 2:", part2)
