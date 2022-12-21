from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym
import json
import math

inpt = [*map(json.loads, read_lines(18))]

nums = "1234567890"

def depths(snail):
    s = json.dumps(snail)
    depth = 0
    prev = None
    result = []
    for c in s:
        if c == "[":
            depth += 1
        elif c == "]":
            if prev in nums:
                result.append(depth)
            depth -= 1
        elif c == "," and prev in nums:
            result.append(depth)
        prev = c
    return result

def values(snail):
    return [*it2.collapse(snail)]

def unpacked(snail):
    return [*zip(values(snail), depths(snail))]

snails = [*map(unpacked, inpt)]

def reduce(snail):
    vs = [*map(first, snail)]
    ds = [*map(second, snail)]
    if 5 in ds:
        i = ds.index(5)
        j = i + 1
        a = vs[i]
        b = vs[j]
        l = [(vs[i-1] + a,ds[i-1])] if i > 0 else []
        r = [(vs[j+1] + b,ds[j+1])] if j+1 < len(vs) else []
        head = snail[0:i-1] if i > 1 else []
        tail = snail[j+2:]
        return reduce(head + l + [(0,4)] + r + tail)
    elif [x for x in vs if x > 9]:
        top = first([x for x in vs if x > 9])
        i = vs.index(top)
        d = ds[i]
        head = snail[0:i]
        tail = snail[i+1:]
        return reduce(head + [(math.floor(top/2), inc(d)), (math.ceil(top/2), inc(d))] + tail)
    else:
        return snail

def add(a,b):
    return reduce([(v, d+1) for v,d in a+b])

def magnitude(snail):
    if len(snail) == 1:
        return snail[0][0]
    vs = [*map(first, snail)]
    ds = [*map(second, snail)]
    d = max(ds)
    i = ds.index(d)
    head = snail[0:i]
    tail = snail[i+2:]
    return magnitude(head + [(3 * vs[i] + 2 * vs[i + 1], dec(d))] + tail)

part1 = magnitude(func.reduce(add, snails))
print("Part 1:", part1)

part2 = max([magnitude(add(snail, other)) for snail in snails for other in snails if snail != other])
print("Part 2:", part2)
