import numpy

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

lines = read_lines(21)

grid=A([list(row) for row in [".#.","..#","###"]])

rules=dict()
for line in lines:
    a,b = line.split(" => ")
    rules[a]=b

def next_symbol(arr):
    for flip in [arr, np.fliplr(arr)]:
        for rot in [flip, np.rot90(flip,1), np.rot90(flip,2), np.rot90(flip,3)]:
            cand="/".join("".join(row) for row in rot)
            if cand in rules:
                return A([list(row) for row in rules[cand].split("/")])

def split(arr,by):
    N = len(arr)
    return arr.reshape(N//by,by,-1,by).swapaxes(1,2)

def combine(arr):
    return arr.swapaxes(1,2).reshape(arr.shape[0]*len(arr[0][0]),-1)

for _ in range(5):
    if len(grid)%2==0:
        subarrays=split(grid,2)
    elif len(grid)%3==0:
        subarrays=split(grid,3)
    grid = combine(A([[next_symbol(suba) for suba in subarow] for subarow in subarrays]))


part1 = np.count_nonzero(grid=="#")
print("Part 1:", part1)

for _ in range(13):
    if len(grid)%2==0:
        subarrays=split(grid,2)
    elif len(grid)%3==0:
        subarrays=split(grid,3)
    grid = combine(A([[next_symbol(suba) for suba in subarow] for subarow in subarrays]))

part2 = np.count_nonzero(grid=='#')
print("Part 2:", part2)
