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

lines = read_lines(10)
nums=[i for i in range(256)]
lengths = [int(n) for n in lines[0].split(",")]
skip_size=0
pos=0
rotations=0
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


part1 = product(nums[:2])
print("Part 1:", part1)

nums=[i for i in range(256)]
lengths = [ord(n) for n in lines[0]]+[17, 31, 73, 47, 23]
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
    dense_hash+=f"{func.reduce(op.xor, sublist):x}"

part2=dense_hash
print("Part 2:", part2)
