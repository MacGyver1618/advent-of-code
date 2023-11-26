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

lines = read_lines(16)

base=[0,1,0,-1]
L=len(lines[0])
masks=[[d for i in range(L+1) for d in [base[i%4]]*k][1:] for k in range(1,L+1)]

def fft(signal):
    return [abs(sum(masks[k][i]*signal[i] for i in range(len(signal))))%10 for k in range(L)]

signal=[*map(int,lines[0])]
for _ in range(100):
    signal=fft(signal)

part1 = "".join(str(i) for i in signal[:8])
print("Part 1:", part1)

# The offset is always greater than L//2, i.e. the base signal
# for digit i is always preceded by i-1 zeros, and followed by
# exactly i ones, i.e. the weights are an upper triangular matrix of ones.

# This means, that the i:th digit is sum(signal[i:]), and we can just subtract
# the i:th element from the previous sum to get i+1:th element.

offset=int(lines[0][:7])
signal=[*map(int,lines[0]*10_000)][offset:]
L=len(signal)

for _ in range(100):
    next_signal=[]
    _sum=sum(signal)
    for i in range(L):
        next_signal+=[_sum%10]
        _sum-=signal[i]
    signal=next_signal

part2 = "".join(str(d) for d in signal[:8])
print("Part 2:", part2)
