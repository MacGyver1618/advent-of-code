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

lines = read_lines(8)
tree=[*map(int,lines[0].split())]

def get_mds(pos):
    children=tree[pos]
    metadata_count=tree[pos+1]
    skip_length=2
    metadata_sum=0
    for _ in range(children):
        skip,mds=get_mds(pos+skip_length)
        skip_length+=skip
        metadata_sum+=mds
    for i in range(pos+skip_length,pos+skip_length+metadata_count):
        metadata_sum+=tree[i]
    return skip_length+metadata_count,metadata_sum
_,part1 = get_mds(0)
print("Part 1:", part1)
def get_val(pos):
    children=tree[pos]
    metadata_count=tree[pos+1]
    skip_length=2
    metadata_sum=0
    if children>0:
        child_vals=[0]*children
        for i in range(children):
            skip,val=get_val(pos+skip_length)
            skip_length+=skip
            child_vals[i]=val
        for i in range(pos+skip_length,pos+skip_length+metadata_count):
            child_index=tree[i]-1
            if child_index<children:
                metadata_sum+=child_vals[child_index]
    else:
        for i in range(pos+skip_length,pos+skip_length+metadata_count):
            metadata_sum+=tree[i]
    return skip_length+metadata_count,metadata_sum

_,part2 = get_val(0)
print("Part 2:", part2)
