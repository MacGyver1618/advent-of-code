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

lines = read_lines(24)
comps=[]
for line in lines:
    comp=tuple(map(int,line.split("/")))
    comps+=[comp]

def look_for(port, bag):
    return [comp for comp in bag if port in comp]

def find_bridges(bridge_so_far, looking_for, remaining):
    candidates = look_for(looking_for, remaining)
    if not candidates:
        yield bridge_so_far
    for cand in candidates:
        bridge=bridge_so_far+[cand]
        next_to_find=cand[1] if cand[0] == looking_for else cand[0]
        remaining_after=[other for other in remaining if other!=cand]
        yield from find_bridges(bridge, next_to_find, remaining_after)

bridges=[bridge for bridge in find_bridges([], 0, comps)]

part1 = max(sum(sum(comp) for comp in bridge) for bridge in bridges)
print("Part 1:", part1)

longest = max(len(bridge) for bridge in bridges)
part2=max(sum(sum(comp) for comp in bridge) for bridge in bridges if len(bridge)==longest)
print("Part 2:", part2)
