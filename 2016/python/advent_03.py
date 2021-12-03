from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

I = lines(3)
tris = [to_nums(re.findall(r"\d+", l)) for l in I]

def is_triangle(arr):
    a,b,c = sorted(arr)
    return a+b>c

print("Part 1:", sum(map(is_triangle, tris)))

def transpose(mat):
    return zip(*mat)

part2 = 0
def trans():
    for i in range(0, len(tris), 3):
        yield from transpose(tris[i:i+3])

print("Part 2:", sum(map(is_triangle, trans())))
