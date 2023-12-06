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

_input = full_input(5)[:-1]
seeds,*maps=_input.split("\n\n")
seeds=[*map(int,seeds.split()[1:])]
traversal=["seed","soil","fertilizer","water","light","temperature","humidity","location"]
mappings=defaultdict(list)

for _map in maps:
    mapping,*ranges=_map.split("\n")
    mapfrom,mapto=mapping.split()[0].split("-to-")
    for _range in ranges:
        deststart,sourcestart,rangelength=map(int,_range.split())
        mappings[(mapfrom,mapto)]+=[(deststart,sourcestart,rangelength)]

lowest=float("inf")


def traverse_seed(seed):
    current = seed
    location = "seed"
    for point in traversal[1:]:
        mapping = mappings[(location, point)]
        _range = [(d, s, l) for d, s, l in mapping if s <= current < s + l]
        if _range:
            d, s, l = _range[0]
            current = current - s + d
        location = point
    return current

part1 = min([traverse_seed(seed) for seed in seeds])
print("Part 1:", part1)

lowest_range=[m for m in mappings[("humidity","location")] if m[0]==0][0]
seed_ranges=[seeds[i:i+2] for i in range(0,len(seeds),2)]
end=0
while True:
    sys.stdout.write(f"\rPart 2: {end}")
    sys.stdout.flush()
    location="location"
    current=end
    for point in traversal[::-1][1:]:
        mapping = mappings[(point, location)]
        _range = [(d, s, l) for d, s, l in mapping if d <= current < d + l]
        if _range:
            d, s, l = _range[0]
            current = current - d + s
        location = point
    if [1 for s,l in seed_ranges if s<=current<s+l]:
        part2=end
        break
    end+=1
print("Part 2:", part2)
