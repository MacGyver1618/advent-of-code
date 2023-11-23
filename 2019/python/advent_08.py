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
layers = [int(c) for c in lines[0]]
layers = [layers[150*i:150*(i+1)] for i in range(len(layers)//150)]
zeros = [layer.count(0) for layer in layers]
least_zeros = zeros.index(min(zeros))
part1_layer = layers[least_zeros]

part1 = part1_layer.count(1)*part1_layer.count(2)
print("Part 1:", part1)

L=len(layers)
print("Part 2:")
for r in range(6):
    s=""
    for c in range(25):
        for l in range(L):
            p=layers[l][r*25+c]
            if p!=2:
                s+=" #"[p]
                break
    print(s)