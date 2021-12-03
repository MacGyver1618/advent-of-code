from advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = lines(2)

keypad = {
    (0,0): 1,
    (0,1): 2,
    (0,2): 3,
    (1,0): 4,
    (1,1): 5,
    (1,2): 6,
    (2,0): 7,
    (2,1): 8,
    (2,2): 9
}

p = 1,1
s = ""
for line in inpt:
    for i in line[:]:
        p += directions[i]
        p = A(list(map(max, zip(p, O))))
        p = A(list(map(min, zip(p, A([2,2])))))
    s += str(keypad[tuple(reversed(p))])

print("Part 1:", s)

p = 0,2
s = ""
keypad = {
    (2,0): "1",
    (1,1): "2",
    (2,1): "3",
    (3,1): "4",
    (0,2): "5",
    (1,2): "6",
    (2,2): "7",
    (3,2): "8",
    (4,2): "9",
    (1,3): "A",
    (2,3): "B",
    (3,3): "C",
    (2,4): "D"
}

for line in inpt:
    for i in line[:]:
        next = p + directions[i]
        p = next if tuple(next) in keypad else p
    s += keypad[tuple(p)]

print("Part 2:", s)
