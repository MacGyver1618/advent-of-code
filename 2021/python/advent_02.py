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

depth = 0
pos = 0

for line in inpt:
    direction, amount = line.split(" ")
    amount = int(amount)
    if direction == "forward":
        pos += amount
    if direction == "down":
        depth += amount
    if direction == "up":
        depth -= amount

print("Part 1:", depth*pos)


depth = 0
pos = 0
aim = 0

for line in inpt:
    direction, amount = line.split(" ")
    amount = int(amount)
    if direction == "forward":
        pos += amount
        depth += amount*aim
    if direction == "down":
        aim += amount
    if direction == "up":
        aim -= amount
print("Part 2:", pos*depth)
