from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(16)

sues = coll.defaultdict(lambda: coll.defaultdict(lambda: -1))
for line in inpt:
    sue, props = line.split(": ", maxsplit=1)
    for prop in props.split(", "):
        k,v = prop.split(": ")
        sues[sue][k] = int(v)

def possible(sue):
    sue = sues[sue]
    return (sue["children"] == 3 or sue["children"] == -1) \
           and (sue["cats"] == 7 or sue["cats"] == -1) \
           and (sue["samoyeds"] == 2 or sue["samoyeds"] == -1) \
           and (sue["pomeranians"] == 3 or sue["pomeranians"] == -1) \
           and (sue["akitas"] == 0 or sue["akitas"] == -1) \
           and (sue["vizslas"] == 0 or sue["vizslas"] == -1) \
           and (sue["goldfish"] == 5 or sue["goldfish"] == -1) \
           and (sue["trees"] == 3 or sue["trees"] == -1) \
           and (sue["cars"] == 2 or sue["cars"] == -1) \
           and (sue["perfumes"] == 1 or sue["perfumes"] == -1)

print("Part 1:", it2.first_true(sues, pred=possible))

def possible2(sue):
    sue = sues[sue]
    return (sue["children"] == 3 or sue["children"] == -1) \
           and (sue["cats"] > 7 or sue["cats"] == -1) \
           and (sue["samoyeds"] == 2 or sue["samoyeds"] == -1) \
           and (sue["pomeranians"] < 3 or sue["pomeranians"] == -1) \
           and (sue["akitas"] == 0 or sue["akitas"] == -1) \
           and (sue["vizslas"] == 0 or sue["vizslas"] == -1) \
           and (sue["goldfish"] < 5 or sue["goldfish"] == -1) \
           and (sue["trees"] > 3 or sue["trees"] == -1) \
           and (sue["cars"] == 2 or sue["cars"] == -1) \
           and (sue["perfumes"] == 1 or sue["perfumes"] == -1)

print("Part 2:", it2.first_true(sues, pred=possible2))
