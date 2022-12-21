from common.advent_lib import *
import collections as coll
import functools as func
import itertools as it
import operator as oper
import re
import more_itertools as it2
import numpy as np
import sympy as sym

inpt = read_lines(8)

part1 = 0

for line in inpt:
    i,o = line.split(" | ")
    o = o.split(" ")
    for t in o:
        l = len(t)
        if l == 2 or l == 3 or l == 4 or l == 7:
            part1 += 1

print("Part 1:", part1)

part2 = 0

outputs = {
    frozenset("abcefg"): "0",
    frozenset("cf"): "1",
    frozenset("acdeg"): "2",
    frozenset("acdfg"): "3",
    frozenset("bcdf"): "4",
    frozenset("abdfg"): "5",
    frozenset("abdefg"): "6",
    frozenset("acf"): "7",
    frozenset("abcdefg"): "8",
    frozenset("abcdfg"): "9"
}

for line in inpt:
    i,o = line.split(" | ")
    o = o.split()
    i = i.split()
    i = [*map(set, sorted(i, key= len))]
    a = i[1].difference(i[0])
    d = set.intersection(i[2], i[3], i[4], i[5])
    f = set.intersection(i[0], i[6], i[7], i[8])
    c = i[0].difference(f)
    g = [x.difference(set.union(a,c,d,f)) for x in i if len(x) == 5 and len(x.difference(set.union(a,c,d,f))) == 1][0]
    b = i[2].difference(set.union(c,d,f))
    e = i[9].difference(set.union(a,b,c,d,f,g))
    num = ""
    for x in o:
        s = ""
        s += "a" if [*a][0] in x else ""
        s += "b" if [*b][0] in x else ""
        s += "c" if [*c][0] in x else ""
        s += "d" if [*d][0] in x else ""
        s += "e" if [*e][0] in x else ""
        s += "f" if [*f][0] in x else ""
        s += "g" if [*g][0] in x else ""
        s = frozenset(s)
        num += outputs[s]
    part2 += int(num)

print("Part 2:", part2)
