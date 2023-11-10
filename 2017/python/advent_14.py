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

lines = read_lines(14)
key=lines[0]

def knot_hash(s):
    nums=[i for i in range(256)]
    lengths = [ord(n) for n in s]+[17, 31, 73, 47, 23]
    skip_size=0
    pos=0
    rotations=0
    for _ in range(64):
        for length in lengths:
            nums = nums[pos:pos+length][::-1]+nums[pos+length:]
            rotation=length+skip_size
            nums=deque(nums)
            nums.rotate(-rotation)
            rotations+=rotation
            skip_size+=1
            nums=list(nums)

    nums=deque(nums)
    nums.rotate(rotations)
    nums=list(nums)

    dense_hash=""
    for i in range(16):
        sublist=nums[16*i:16*(i+1)]
        dense_hash+=f"{func.reduce(op.xor, sublist):02x}"
    return dense_hash

grid=[[0]*128]*128
for i in range(128):
    key2 = f"{key}-{i}"
    temp = f"{int(knot_hash(key2), 16):0128b}"
    grid[i] = temp
part1 = sum(1 for y in range(128) for x in range(128) if grid[y][x] == '1')
print("Part 1:", part1)


def find_region(p):
    seen = {p}
    Q = deque(seen)
    while Q:
        cur = Q.popleft()
        for n in adjacent(cur):
            n = tuple(n)
            r,c=n
            if 0<=r<128 and 0<=c<128 and grid[r][c]=='1' and n not in seen:
                Q.append(n)
                seen.add(n)
    return frozenset(seen)


ones=[(r,c) for r in range(128) for c in range(128) if grid[r][c]=='1']
regions=set()
queue=deque(ones)
discovered=set()
while queue:
    square = queue.pop()
    if square in discovered:
        continue
    region=find_region(square)
    regions.add(region)
    discovered = discovered.union(region)

part2=len(regions)
print("Part 2:", part2)
