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

toks = read_lines(15)[0].split(",")
def _hash(tok):
    val = 0
    for char in tok:
        val += ord(char)
        val *= 17
        val %= 256
    return val

part1 = sum(_hash(tok) for tok in toks)
print("Part 1:", part1)

boxes=[{} for _ in range(256)]
for tok in toks:
    label=re.findall("\\w+",tok)[0]
    box=boxes[_hash(label)]
    if "=" in tok:
        box[label] = int(tok.split("=")[-1])
    else:
        box.pop(label,0)

tot=0
for i,box in enumerate(boxes,start=1):
    for j,focal in enumerate(box.values(),start=1):
        tot+=i*j*focal

part2=tot
print("Part 2:", part2)
